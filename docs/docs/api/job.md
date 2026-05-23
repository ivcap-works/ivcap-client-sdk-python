# Job

A `Job` represents a running or completed execution of an IVCAP service. Jobs are
created by calling `service.request_job()` and tracked via `job.refresh()`.

## Quick Reference

```python
import time
from ivcap_client import JobStatus

# Submit
job = service.request_job(req)
print(f"Job ID: {job.id}")

# Poll
while not job.finished:
    time.sleep(5)
    job.refresh()

# Check result
if job.status() == JobStatus.SUCCEEDED:
    print(job.result)
```

## JobStatus Enum

`JobStatus` represents all possible states of a job:

| Value | Meaning |
|---|---|
| `UNKNOWN` | Status cannot be determined |
| `PENDING` | Job created, awaiting a dispatcher slot |
| `SCHEDULED` | Dispatcher has provisioned compute resources |
| `EXECUTING` | Service container is actively processing |
| `SUCCEEDED` | Job completed successfully; result is available |
| `FAILED` | Service reported a business-logic failure |
| `ERROR` | Platform-level error (OOM, timeout, infrastructure) |

## Class Documentation

::: ivcap_client.job.Job

## Enum Documentation

::: ivcap_client.job.JobStatus
