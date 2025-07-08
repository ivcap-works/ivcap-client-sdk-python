#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from __future__ import annotations # postpone evaluation of annotations
from typing import TYPE_CHECKING, Dict, List, Optional

from ivcap_client.service import Service
from ivcap_client.types import Response
if TYPE_CHECKING:
    from ivcap_client.ivcap import IVCAP, URN

import datetime
from dataclasses import dataclass
from datetime import datetime


from ivcap_client.api.service import service_job_list, service_job_read
from ivcap_client.aspect import Aspect
from ivcap_client.models.job_list_item import JobListItem
from ivcap_client.models.job_list_rt import JobListRT
from ivcap_client.models.job_status_rt_status import JobStatusRTStatus
from ivcap_client.models.job_status_rt import JobStatusRT
from ivcap_client.models.parameter_t import ParameterT
from ivcap_client.utils import BaseIter, Links, _set_fields, _unset, process_error, set_page

from enum import Enum

class JobStatus(Enum):
    UNKNOWN = "unknown"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    EXECUTING = "executing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ERROR = "error"

    @classmethod
    def from_string(cls, s: str) -> "JobStatus":
        try:
            return cls(s)
        except ValueError:
            return cls.UNKNOWN

@dataclass
class Job:
    """This class represents a particular job placed
    or executed at a particular IVCAP deployment"""

    id: str
    name: Optional[str] = None
    request_content_type: Optional[str] = None
    result_content_type: Optional[str] = None
    requested_at: Optional[datetime.datetime] = None
    started_at: Optional[datetime.datetime] = None
    finished_at: Optional[datetime.datetime] = None

    policy: Optional[URN] = None
    account: Optional[URN] = None

    @classmethod
    def _from_list_item(cls, item: JobListItem, ivcap: IVCAP):
        kwargs = item.to_dict()
        return cls(ivcap, **kwargs)

    @classmethod
    def from_create_order_response(cls, response: Response, service: Service):
        if response.status_code == 202:
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
        p = ["id", "name", "request-content-type", "result-content-type", "requested-at", "started-at", "finished-at", "policy", "account"]
        hp = ["status", "request-content", "result-content"]
        _set_fields(self, p, hp, kwargs)
        self._status = JobStatus.from_string(self._status)
        if self._service_obj == None and self._service != None:
            self._service_obj = Service(id=self._service)

    @property
    def urn(self) -> str:
        return self.id

    def status(self, refresh=True) -> JobStatus:
        if refresh:
            self.refresh()
        return self._status

    @property
    def finished(self):
        return self._status in [JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.ERROR]

    @property
    def service(self) -> Service:
        return self._service

    def refresh(self) -> Job:
        if self.finished:
            return self # no need to refresh

        kwargs = {
            "client": self._ivcap._client,
            "id": self.id,
            "service_id": self._service,
            "with_request_content": self._request_content == None,
            "with_result_content": self._result_content == None,
        }
        r = service_job_read.sync_detailed(**kwargs)
        if r.status_code >= 300:
            return process_error('place_job', r)
        kwargs = r.parsed.to_dict()
        self.__update__(**kwargs)
        return self

    def __repr__(self):
        status = self._status if self._status else '???'
        return f"<Job id={self.id}, status={status}>"

    def __hash__(self):
        return hash((self.id))

class JobIter(BaseIter[Job, JobListItem]):
    def __init__(self, ivcap: 'IVCAP', **kwargs):
        super().__init__(ivcap, **kwargs)

    def _next_el(self, el) -> Job:
        return Job._from_list_item(el, self._ivcap)

    def _get_list(self) -> List[JobListItem]:
        r = job_list.sync_detailed(**self._kwargs)
        if r.status_code >= 300 :
            return process_error('artifact_list', r)
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
