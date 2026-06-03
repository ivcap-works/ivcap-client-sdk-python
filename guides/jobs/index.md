# Running Jobs

This guide covers submitting jobs to IVCAP services and monitoring their execution.

## Overview

A **Job** is the tracked execution of one service invocation. When you call
`service.request_job(data)`, the platform:

1. Creates a job record (`urn:ivcap:job:<uuid>`) with status `pending`
2. Selects the appropriate dispatcher (Lambda, Batch, Nextflow, or Argo)
3. Launches the service container in Kubernetes
4. Runs the computation and writes results back to the Datafabric

## Job Lifecycle

```
pending → scheduled → executing → succeeded
                                → failed
                                → error
```

| Status | Meaning |
|---|---|
| `pending` | Job record created, waiting for a dispatcher slot |
| `scheduled` | Dispatcher has provisioned the execution environment |
| `executing` | Service container is processing the job |
| `succeeded` | Service reported success; result is available |
| `failed` | Service reported failure (business-logic failure) |
| `error` | Platform-level error (infrastructure, timeout, OOM) |

## Submitting a Job

### Fire and check (non-blocking)

```python
import io, json
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()
svc = ivcap.get_service("urn:ivcap:service:<uuid>")

# Submit — returns immediately (timeout=0)
# request_job accepts a Pydantic BaseModel, a dataclass, or an IO[str] (JSON)
job = svc.request_job(io.StringIO(json.dumps({"param": "value"})))
print(f"Created job: {job.id}")
```

### With a Pydantic model

```python
Model = svc.request_model
req = Model(duration_seconds=6, target_cpu_percent=90)
job = svc.request_job(req)
```

### Blocking (wait for completion server-side)

Pass a `timeout` in seconds. The API gateway holds the connection open until the job
completes or the timeout elapses:

```python
# Block up to 120 seconds server-side
job = svc.request_job(req, timeout=120)

# Block indefinitely
job = svc.request_job(req, timeout=None)
```

> **Note:** `timeout=0` (the default) means "submit and return immediately with 202 Accepted".
> The gateway does not wait; poll with `job.refresh()`.

### With a raw JSON string or IO stream

```python
import io

payload = '{"wordle": {"maxattempts": 2, "thinking_time": 1}}'
job = svc.request_job(io.StringIO(payload))
```

## Polling for Completion

```python
import time
from ivcap_client import JobStatus

while not job.finished:
    time.sleep(5)
    job.refresh()             # pull latest state from server

print(job.status())           # JobStatus.SUCCEEDED / .FAILED / .ERROR
print(job.result)             # parsed response body
```

`job.finished` is `True` when status is `SUCCEEDED`, `FAILED`, or `ERROR`.

## Accessing the Result

```python
if job.status() == JobStatus.SUCCEEDED:
    result = job.result      # dict / object
    print(result)
```

> **Under the hood:** `job.refresh()` reads the `urn:ivcap:schema.job.2` aspect from
> the Datafabric. The result is stored as a `urn:ivcap:schema.job-result.1` aspect —
> accessing `job.result` may trigger a second network round-trip.

## Job Properties

| Property/Method | Description |
|---|---|
| `job.id` | URN of the job |
| `job.status()` | Current `JobStatus` (re-fetched from server) |
| `job.finished` | `True` if SUCCEEDED, FAILED, or ERROR |
| `job.succeeded` | `True` only if SUCCEEDED |
| `job.result` | Result payload (fetched on demand) |
| `job.refresh()` | Pull latest state from the server |
| `job.requested_at` | When the job was submitted |
| `job.started_at` | When execution began |
| `job.finished_at` | When execution ended |

## Batch Job Monitoring

Monitor many jobs simultaneously:

```python
import csv
from time import sleep, time

jobs = [svc.request_job(req) for _ in range(10)]

with open("results.csv", "w", newline="") as f:
    w = csv.writer(f)
    start = time()
    while True:
        sleep(10)
        elapsed = int(time() - start)
        for j in jobs:
            j.refresh()
            w.writerow([elapsed, j.id, j.status().value])
        f.flush()
        done = sum(1 for j in jobs if j.finished)
        print(f"Progress: {done}/{len(jobs)}")
        if done == len(jobs):
            break
```

## Handling Job Failures

```python
from ivcap_client import JobStatus

while not job.finished:
    time.sleep(5)
    job.refresh()

if job.status() == JobStatus.SUCCEEDED:
    print("Done:", job.result)
elif job.status() == JobStatus.FAILED:
    print("Job reported failure (check service logs)")
elif job.status() == JobStatus.ERROR:
    print("Platform-level error (infrastructure, OOM, timeout)")
```

## See Also

- [Discovering Services](services.md) — Find and inspect services
- [Async Usage](async-usage.md) — Async job patterns and parallel execution
- [Error Handling](error-handling.md) — Exception types and retry strategies
- [API Reference: Job](../api/job.md) — Full `Job` class documentation
- [Examples: Job Workflows](../examples/jobs.md) — Ready-to-run scripts
