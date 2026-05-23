# Error Handling

This guide covers all exception types raised by the IVCAP Client SDK and how to handle them.

## Exception Hierarchy

All IVCAP exceptions inherit from `IvcapError`:

```
IvcapError
├── IvcapApiError          # HTTP error from the platform API
│   ├── NotAuthorizedException   # 401/403
│   └── ResourceNotFound         # 404 (service, artifact, order not found)
├── AmbiguousRequest       # get_service_by_name matched multiple services
└── MissingParameterValue  # required parameter missing when creating an aspect
```

## Importing Exceptions

```python
from ivcap_client.exception import (
    IvcapError,               # base class for all IVCAP exceptions
    IvcapApiError,            # HTTP error from the API (.status_code, .operation)
    NotAuthorizedException,   # HTTP 401/403
    ResourceNotFound,         # service / artifact / order not found
    AmbiguousRequest,         # get_service_by_name matched more than one service
    MissingParameterValue,    # required parameter missing
)
```

## Common Patterns

### Service lookup

```python
from ivcap_client.exception import ResourceNotFound, AmbiguousRequest

try:
    service = ivcap.get_service_by_name("my-service")
except ResourceNotFound as e:
    print(f"Service not found: {e.resource}")
except AmbiguousRequest as e:
    print(f"Multiple services match: {e}")
```

### API errors (upload, download, etc.)

```python
from ivcap_client.exception import IvcapApiError

try:
    artifact = ivcap.upload_artifact(file_path="/tmp/data.csv")
except IvcapApiError as e:
    print(f"Upload failed [{e.status_code}]: {e}")
    print(f"Operation: {e.operation}")
```

### Authorization errors

```python
from ivcap_client.exception import NotAuthorizedException

try:
    for svc in ivcap.list_services():
        print(svc)
except NotAuthorizedException:
    print("JWT token is invalid or expired — refresh with: ivcap context get access-token")
```

## Job Failure Detection

There are two kinds of job non-success outcomes:

| Status | Cause | Action |
|---|---|---|
| `FAILED` | Service reported a business-logic failure | Check service logs; fix input data |
| `ERROR` | Platform-level error (OOM, timeout, infra) | Retry; check cluster health |

```python
from ivcap_client import JobStatus

while not job.finished:
    import time; time.sleep(5)
    job.refresh()

if job.status() == JobStatus.SUCCEEDED:
    print("Done:", job.result)
elif job.status() == JobStatus.FAILED:
    print("Job failed — check the service's error log")
elif job.status() == JobStatus.ERROR:
    print("Platform error — consider retrying")
```

## Retry Patterns

For transient failures, implement a simple retry loop:

```python
import time
from ivcap_client.exception import IvcapApiError

def submit_with_retry(svc, req, max_retries=3, delay=10):
    for attempt in range(max_retries):
        try:
            return svc.request_job(req)
        except IvcapApiError as e:
            if attempt < max_retries - 1 and e.status_code >= 500:
                print(f"Attempt {attempt + 1} failed ({e.status_code}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise
```

## Catching All IVCAP Errors

```python
from ivcap_client.exception import IvcapError

try:
    service = ivcap.get_service_by_name("my-service")
    job = service.request_job(req)
except IvcapError as e:
    print(f"IVCAP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise
```

## See Also

- [Running Jobs](jobs.md) — Job status values and failure modes
- [Async Usage](async-usage.md) — Error handling in async code
- [API Reference: Exceptions](../api/exceptions.md) — Full exception class documentation
