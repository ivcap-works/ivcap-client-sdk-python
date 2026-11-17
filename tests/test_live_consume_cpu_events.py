"""Live end-to-end check of job events from the test-batch ``consume_cpu`` target.

Runs against a real IVCAP deployment, so it needs ``IVCAP_URL`` and ``IVCAP_JWT``
in the environment and is skipped otherwise.
"""

import io
import json
import os
from typing import Any

import pytest

from ivcap_client.ivcap import IVCAP
from ivcap_client.job import Job, JobEvent, JobStatus

TEST_BATCH_SERVICE_ID = "urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948"
JOB_TIMEOUT_SECONDS = 300

STEP_START_SCHEMA = "urn:ivcap:schema:service.event.step.start.1"
STEP_FINISH_SCHEMA = "urn:ivcap:schema:service.event.step.finish.1"
STEP_ERROR_SCHEMA = "urn:ivcap:schema:service.event.step.error.1"

requires_ivcap = pytest.mark.skipif(
    not (os.getenv("IVCAP_URL") and os.getenv("IVCAP_JWT")),
    reason="needs IVCAP_URL and IVCAP_JWT for a live IVCAP deployment",
)


def _schemas(obj: Any) -> set[str]:
    """Collect every ``$schema`` value found anywhere in a parsed event payload."""
    found: set[str] = set()
    if isinstance(obj, dict):
        if isinstance(obj.get("$schema"), str):
            found.add(obj["$schema"])
        for v in obj.values():
            found |= _schemas(v)
    elif isinstance(obj, list):
        for v in obj:
            found |= _schemas(v)
    return found


def _run_consume_cpu(params: dict) -> tuple[list[JobEvent], Job]:
    """Submit a test-batch job with the given request body and wait for its event stream to end."""
    svc = IVCAP().get_service(TEST_BATCH_SERVICE_ID)
    job = svc.request_job(io.StringIO(json.dumps(params)))

    events: list[JobEvent] = []
    thread = job.watch_events(events.append, background=True)
    thread.join(timeout=JOB_TIMEOUT_SECONDS)
    assert not thread.is_alive(), "event stream did not reach a terminal event"
    return events, job


def _with_schema(events: list[JobEvent], schema: str) -> list[str]:
    return [json.dumps(ev.data) for ev in events if schema in _schemas(ev.data)]


@requires_ivcap
def test_consume_cpu_success_emits_progress_and_finish_events():
    events, job = _run_consume_cpu(
        {
            "consume_cpu": {
                "duration_seconds": 20,
                "progress_interval_seconds": 2,
                "target_cpu_percent": 60,
            }
        },
    )

    step_starts = _with_schema(events, STEP_START_SCHEMA)
    assert step_starts, "no consume_compute step.start event received"
    assert "Consuming CPU for 20 seconds" in step_starts[0]

    progress = [ev for ev in events if "progress:" in json.dumps(ev.data)]
    assert len(progress) >= 8, f"expected about 9 progress events, got {len(progress)}"

    finish = _with_schema(events, STEP_FINISH_SCHEMA)
    assert finish, "no end-of-service step.finish event received"
    assert "actual_duration" in finish[-1]
    assert not _with_schema(events, STEP_ERROR_SCHEMA)
    assert job.status() == JobStatus.SUCCEEDED


@requires_ivcap
def test_consume_cpu_exception_emits_error_event_and_fails():
    events, job = _run_consume_cpu(
        {
            "consume_cpu": {
                "duration_seconds": 4,
                "target_cpu_percent": 50,
                "throw_exception_at_end": True,
            }
        },
    )

    errors = _with_schema(events, STEP_ERROR_SCHEMA)
    assert errors, "no end-of-service step.error event received"
    assert "throwing an exception as requested" in errors[-1]
    # The platform reports a service that raised as ERROR, not FAILED.
    assert job.status() == JobStatus.ERROR


@requires_ivcap
def test_nested_consume_cpu_exception_emits_error_and_error_result():
    events, job = _run_consume_cpu(
        {
            "consume_cpu": {
                "duration_seconds": 2,
                "target_cpu_percent": 60,
                "throw_exception_at_end": True,
            }
        },
    )

    step_starts = _with_schema(events, STEP_START_SCHEMA)
    assert step_starts, "no consume_compute step.start event received"
    assert "Consuming CPU for 2 seconds at 60%" in step_starts[0]

    errors = _with_schema(events, STEP_ERROR_SCHEMA)
    assert errors, "no end-of-service step.error event received"
    assert "throwing an exception as requested" in errors[-1]

    results = [ev for ev in events if ev.data.get("type") == "ivcap.job.result"]
    assert results, "no job.result event received"
    assert "service.error" in results[-1].data["data"]["content-type"]

    # The platform reports a service that raised as ERROR, not FAILED.
    assert job.status() == JobStatus.ERROR


@requires_ivcap
def test_consume_cpu_exit_code_emits_finish_event_and_fails():
    events, job = _run_consume_cpu(
        {
            "consume_cpu": {
                "duration_seconds": 4,
                "target_cpu_percent": 50,
                "exit_code_at_end": 1,
            }
        },
    )

    finish = _with_schema(events, STEP_FINISH_SCHEMA)
    assert any("exiting with code 1" in msg for msg in finish)
    assert job.status() == JobStatus.ERROR
