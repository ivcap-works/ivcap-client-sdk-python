import io
import json
import threading

import httpx
import pytest

from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import IvcapError
from ivcap_client.ivcap import IVCAP
from ivcap_client.job import Job, JobEvent, _parse_sse
from ivcap_client.service import Service

BASE_URL = "http://test"
SERVICE_ID = "urn:ivcap:service:abc"
JOB_ID = "urn:ivcap:job:123"
EVENTS_PATH = f"/1/services2/{SERVICE_ID}/jobs/{JOB_ID}/events"


def _sse_body(*events: tuple[str, dict]) -> str:
    return "".join(f"id: {eid}\ndata: {json.dumps(data)}\n\n" for eid, data in events)


def _ivcap_with(handler) -> IVCAP:
    iv = IVCAP(url=BASE_URL, token="token")
    iv._client = AuthenticatedClient(
        base_url=BASE_URL,
        token="token",
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return iv


def test_parse_sse_yields_events_and_ignores_comments():
    lines = [
        ": keep-alive",
        "id: 1",
        "event: message",
        'data: {"type": "ivcap.job.executing"}',
        "",
        "id: 2",
        "data: not-json",
        "data: second line",
        "",
    ]
    events = list(_parse_sse(lines))

    assert events == [
        JobEvent(id="1", event="message", data={"type": "ivcap.job.executing"}),
        JobEvent(id="2", event=None, data="not-json\nsecond line"),
    ]


def test_watch_events_stops_on_terminal_event_and_sends_job_path():
    seen_paths: list[str] = []
    body = _sse_body(
        ("1", {"type": "ivcap.job.executing"}),
        ("2", {"type": "ivcap.job.succeeded"}),
    )

    def handler(request: httpx.Request) -> httpx.Response:
        seen_paths.append(request.url.path)
        assert request.headers.get("Accept") == "text/event-stream"
        assert request.headers.get("Authorization") == "Bearer token"
        return httpx.Response(200, content=body.encode())

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)
    received: list[JobEvent] = []

    job.watch_events(received.append)

    assert seen_paths == [EVENTS_PATH]
    assert [e.id for e in received] == ["1", "2"]


def test_watch_events_reconnects_with_last_event_id_until_terminal():
    calls: list[str | None] = []
    responses = [
        _sse_body(("10", {"type": "ivcap.job.scheduled"})),  # stream closes early
        _sse_body(("11", {"data": {"phase": "Succeeded"}})),
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.headers.get("Last-Event-ID"))
        return httpx.Response(200, content=responses[len(calls) - 1].encode())

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)
    received: list[JobEvent] = []

    job.watch_events(received.append, reconnect_delay=0)

    assert calls == [None, "10"]
    assert [e.id for e in received] == ["10", "11"]


def test_watch_events_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "not found"})

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)

    with pytest.raises(IvcapError):
        job.watch_events(lambda ev: None)


def test_watch_events_reconnects_after_dropped_connection():
    calls: list[str | None] = []
    body = _sse_body(("5", {"type": "ivcap.job.succeeded"}))

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.headers.get("Last-Event-ID"))
        if len(calls) == 1:
            raise httpx.RemoteProtocolError("server closed connection")
        return httpx.Response(200, content=body.encode())

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)
    received: list[JobEvent] = []

    job.watch_events(received.append, reconnect_delay=0)

    assert calls == [None, None]
    assert [e.id for e in received] == ["5"]


def test_watch_events_callback_false_stops_immediately():
    calls = 0
    body = _sse_body(
        ("1", {"type": "ivcap.job.executing"}), ("2", {"type": "ivcap.job.executing"})
    )

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(200, content=body.encode())

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)
    received: list[JobEvent] = []

    def callback(ev: JobEvent) -> bool:
        received.append(ev)
        return False

    job.watch_events(callback, reconnect_delay=0)

    assert calls == 1
    assert [e.id for e in received] == ["1"]


def test_watch_events_background_returns_immediately_and_calls_back_in_thread():
    release = threading.Event()
    thread_names: list[str] = []
    received: list[JobEvent] = []
    body = _sse_body(
        ("1", {"type": "ivcap.job.executing"}), ("2", {"type": "ivcap.job.succeeded"})
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body.encode())

    def callback(ev: JobEvent) -> bool:
        thread_names.append(threading.current_thread().name)
        release.wait(timeout=5)
        received.append(ev)
        return True

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)
    thread = job.watch_events(callback, background=True)

    assert isinstance(thread, threading.Thread)
    assert thread.is_alive()  # returned before any callback could finish
    release.set()
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert thread_names and set(thread_names) == {thread.name}
    assert [e.id for e in received] == ["1", "2"]


def test_watch_events_blocking_delivers_on_calling_thread():
    thread_names: list[str] = []
    body = _sse_body(("1", {"type": "ivcap.job.succeeded"}))

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=body.encode())

    job = Job(_ivcap_with(handler), id=JOB_ID, service=SERVICE_ID)

    job.watch_events(lambda ev: thread_names.append(threading.current_thread().name))

    assert thread_names == [threading.current_thread().name]


def test_request_job_with_on_event_watches_until_done():
    seen: list[tuple[str, str]] = []
    body = _sse_body(("1", {"type": "ivcap.job.failed"}))

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, request.url.path))
        if request.method == "POST":
            return httpx.Response(202, json={"job-id": JOB_ID})
        return httpx.Response(200, content=body.encode())

    svc = Service(_ivcap_with(handler), id=SERVICE_ID)
    received: list[JobEvent] = []

    job = svc.request_job(io.StringIO('{"x": 1}'), on_event=received.append)

    assert job.id == JOB_ID
    assert seen == [
        ("POST", f"/1/services2/{SERVICE_ID}/jobs"),
        ("GET", EVENTS_PATH),
    ]
    assert [e.id for e in received] == ["1"]
