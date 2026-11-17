#
# Copyright (c) 2023-2026 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations  # postpone evaluation of annotations

import json
import threading
import time
from collections.abc import Awaitable, Callable, Iterable, Iterator
from typing import TYPE_CHECKING, Any

import httpx

from ivcap_client.service import Service
from ivcap_client.types import Response

if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import datetime
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from ivcap_client.api.service import service_job_list, service_job_read
from ivcap_client.models.job_list_item import JobListItem
from ivcap_client.models.job_list_rt import JobListRT
from ivcap_client.models.parameter_t import ParameterT
from ivcap_client.utils import BaseIter, Links, _set_fields, _unset, process_error


class JobStatus(Enum):
    UNKNOWN = "unknown"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ERROR = "error"

    @classmethod
    def from_string(cls, s: str) -> JobStatus:
        try:
            return cls(s)
        except ValueError:
            return cls.UNKNOWN


# HTTP statuses on the events stream that mean "reconnect", not "fail"
_RECONNECTABLE_STATUS_CODES = {408, 502, 503, 504}

_TERMINAL_PHASES = {"Succeeded", "Failed", "Error"}
_TERMINAL_EVENT_TYPES = {
    "ivcap.job.completed",
    "ivcap.job.error",
    "ivcap.job.failed",
    "ivcap.job.succeeded",
}
# ``ivcap.job.status`` events carry the job state in ``data.status``
_TERMINAL_JOB_STATUSES = {"succeeded", "failed", "error"}


@dataclass
class JobEvent:
    """An event emitted for a job, as received from the SSE event stream.

    ``data`` is the parsed JSON payload, or the raw string if it is not JSON.
    ``type``, ``schema`` and ``timestamp`` are taken from that JSON envelope,
    e.g. ``ivcap.job.result`` / ``urn:ivcap:schema:job.result.1``.
    """

    id: str | None
    event: str | None
    data: Any
    type: str | None = None
    schema: str | None = None
    timestamp: str | None = None


def _parse_sse(lines: Iterable[str]) -> Iterator[JobEvent]:
    """Minimal Server-Sent Events parser yielding one JobEvent per block."""
    event_id: str | None = None
    event_type: str | None = None
    data_lines: list[str] = []
    for line in lines:
        if line == "":
            if data_lines:
                raw = "\n".join(data_lines)
                try:
                    data = json.loads(raw)
                except ValueError:
                    data = raw
                envelope = data if isinstance(data, dict) else {}
                yield JobEvent(
                    id=event_id,
                    event=event_type,
                    data=data,
                    type=envelope.get("type"),
                    schema=envelope.get("schema"),
                    timestamp=envelope.get("timestamp"),
                )
            event_id, event_type, data_lines = None, None, []
        elif line.startswith(":"):
            continue  # comment / keep-alive
        else:
            name, _, value = line.partition(":")
            value = value[1:] if value.startswith(" ") else value
            if name == "id":
                event_id = value
            elif name == "event":
                event_type = value
            elif name == "data":
                data_lines.append(value)


def _is_terminal_job_event(ev: JobEvent) -> bool:
    if not isinstance(ev.data, dict):
        return False
    inner = ev.data.get("data")
    if isinstance(inner, dict):
        if inner.get("phase") in _TERMINAL_PHASES:
            return True
        if (
            ev.data.get("type") == "ivcap.job.status"
            and inner.get("status") in _TERMINAL_JOB_STATUSES
        ):
            return True
    return ev.data.get("type") in _TERMINAL_EVENT_TYPES


@dataclass
class Job:
    """This class represents a particular job placed
    or executed at a particular IVCAP deployment"""

    id: str
    name: str | None = None
    request_content_type: str | None = None
    result_content_type: str | None = None
    requested_at: datetime.datetime | None = None
    started_at: datetime.datetime | None = None
    finished_at: datetime.datetime | None = None

    policy: URN | None = None
    account: URN | None = None

    @classmethod
    def _from_list_item(cls, item: JobListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    @classmethod
    def from_create_job_response(cls, response: Response, service: Service):
        if response.status_code == 200:
            kwargs = {
                "id": response.headers.get("ivcap-job-id"),
                "service": service,
                "result-content": response.json(),
                "result-content-type": response.headers.get("content-type"),
            }
            return cls(service._ivcap, **kwargs)
        elif response.status_code == 202:
            j = response.json()
            id = j.get("job-id")
            return cls(service._ivcap, id=id, service=service)
        else:
            raise ("not implemented, yet")

    def __init__(self, ivcap: IVCAP, **kwargs):
        if not ivcap:
            raise ValueError("missing 'ivcap' argument")
        self._ivcap = ivcap
        service = kwargs.pop("service")
        if service is not None:
            if isinstance(service, Service):
                self._service_obj = service
                self._service = service.id
            else:
                self._service_obj = None
                self._service = service
        self._request_content = None
        self._result_content = None
        self.__update__(**kwargs)

    def __update__(self, **kwargs):
        p = [
            "id",
            "name",
            "request-content-type",
            "result-content-type",
            "requested-at",
            "started-at",
            "finished-at",
            "policy",
            "account",
        ]
        hp = ["status", "request-content", "result-content"]
        _set_fields(self, p, hp, kwargs)
        self._status = JobStatus.from_string(self._status)
        if self._service_obj == None and self._service != None:
            self._service_obj = Service(self._ivcap, id=self._service)

    @property
    def urn(self) -> str:
        return self.id

    def status(self, refresh=True) -> JobStatus:
        if refresh:
            self.refresh()
        return self._status

    async def status_async(self, refresh=True) -> Awaitable[JobStatus]:
        if refresh:
            await self.refresh_async()
        return self._status

    @property
    def finished(self):
        if self._finished:
            return True
        self.refresh()
        return self._finished

    @property
    def _finished(self):
        return self._status in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.ERROR]

    async def finished_async(self) -> Awaitable[bool]:
        if self._status in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.ERROR]:
            return True
        await self.refresh_async()
        return self._status in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.ERROR]

    async def wait_for_finished_async(
        self, max_wait_time: float | None = None, poll_interval: float = 5.0
    ) -> Awaitable[Job]:
        import asyncio

        start_time = datetime.now()
        while not await self.finished_async():
            if max_wait_time is not None:
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed >= max_wait_time:
                    raise TimeoutError(
                        f"Job '{self.id}' did not finish within {max_wait_time} seconds"
                    )
            await asyncio.sleep(poll_interval)
        return self

    @property
    def succeeded(self):
        return self.finished and self._status == JobStatus.SUCCEEDED

    @property
    async def succeeded_async(self):
        finished = await self.finished_async()
        return finished and self._status == JobStatus.SUCCEEDED

    @property
    def service(self) -> Service:
        return self._service

    @property
    def result(self):
        if self._result_content == None:
            self.refresh()
        return self._result_content

    async def result_async(self):
        if self._result_content == None:
            await self.refresh_async()
        return self._result_content

    def refresh(self) -> Job:
        if self._finished:
            return self  # no need to refresh

        kwargs = self._refresh_top()
        r = service_job_read.sync_detailed(**kwargs)
        return self._refresh_bottom(r)

    async def refresh_async(self) -> Awaitable[Job]:
        if self._finished:
            return self  # no need to refresh

        kwargs = self._refresh_top()
        r = await service_job_read.asyncio_detailed(**kwargs)
        return self._refresh_bottom(r)

    def _refresh_top(self):
        return {
            "client": self._ivcap._client,
            "id": self.id,
            "service_id": self._service,
            "with_request_content": self._request_content == None,
            "with_result_content": self._result_content == None,
        }

    def _refresh_bottom(self, r: Response) -> Job:
        if r.status_code >= 300:
            return process_error("place_job", r)
        kwargs = r.parsed.to_dict()
        self.__update__(**kwargs)
        return self

    def watch_events(
        self,
        callback: Callable[[JobEvent], bool | None],
        reconnect_delay: float = 3.0,
        background: bool = False,
    ) -> Job | threading.Thread:
        """Stream this job's events and call ``callback`` for each one.

        The callback returns ``False`` to stop watching. Returning ``True`` or
        ``None`` keeps watching. Watching also stops after a terminal event
        (succeeded / failed / error) has been delivered.

        If the server closes the stream, for example after a long period without
        events, or the connection drops, it is re-opened after ``reconnect_delay``
        seconds and resumes after the last received event.

        With ``background=True`` the watch runs in a daemon thread, the callback
        is called from that thread, and the ``threading.Thread`` is returned
        immediately.
        """
        if background:
            thread = threading.Thread(
                target=self._watch_events_loop,
                args=(callback, reconnect_delay),
                name=f"ivcap-job-events-{self.id}",
                daemon=True,
            )
            thread.start()
            return thread
        self._watch_events_loop(callback, reconnect_delay)
        return self

    def _watch_events_loop(
        self, callback: Callable[[JobEvent], bool | None], reconnect_delay: float
    ) -> None:
        last_id: str | None = None

        def on_event(ev: JobEvent) -> bool:
            nonlocal last_id
            if ev.id:
                last_id = ev.id
            keep_going = callback(ev) is not False
            return keep_going and not _is_terminal_job_event(ev)

        while True:
            try:
                if not self._stream_events(last_id, on_event):
                    return
            except httpx.TransportError:
                pass  # connection dropped; reconnect below
            time.sleep(reconnect_delay)

    def _stream_events(
        self, last_event_id: str | None, on_event: Callable[[JobEvent], bool]
    ) -> bool:
        """Read one SSE connection. Returns False if ``on_event`` asked to stop,
        True if the server closed the stream."""
        headers = {"Accept": "text/event-stream"}
        if last_event_id:
            headers["Last-Event-ID"] = last_event_id
        url = f"/1/services2/{self._service}/jobs/{self.id}/events"
        with self._ivcap._client.get_httpx_client().stream(
            "GET", url, headers=headers, timeout=None
        ) as r:
            if r.status_code in _RECONNECTABLE_STATUS_CODES:
                # 504 event-timeout is the ingress closing an idle stream; 502/503/408
                # are transient gateway or server conditions. Reconnect from last_event_id.
                r.read()
                return True
            if r.status_code >= 300:
                r.read()
                return process_error("job_events", r)
            for ev in _parse_sse(r.iter_lines()):
                if not on_event(ev):
                    return False
        return True

    def __repr__(self):
        status = self._status if self._status else "???"
        return f"<Job id={self.id}, status={status}>"

    def __hash__(self):
        return hash(self.id)


class JobIter(BaseIter[Job, JobListItem]):
    def __init__(self, ivcap: IVCAP, **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Job:
        return Job._from_list_item(el, self._ivcap)

    def _get_list(self) -> list[JobListItem]:
        r = service_job_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300:
            return process_error("artifact_list", r)
        l: JobListRT = r.parsed
        self._links = Links(l.links)
        return l.items


@dataclass(init=False)
class JobParameter:
    name: str
    value: any

    def __init__(self, p: ParameterT):
        self.name = _unset(p.name)
        self.value = _unset(p.value)
