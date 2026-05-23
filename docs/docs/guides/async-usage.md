# Async Usage

The IVCAP Client SDK provides `_async` variants of all major operations for use with
Python's `asyncio`. This is especially useful for running many jobs in parallel.

## When to Use Async

- **Parallel jobs** — submit dozens or hundreds of jobs and wait for all of them concurrently
- **Async applications** — integrate IVCAP into FastAPI, aiohttp, or other async frameworks
- **Responsive notebooks** — avoid blocking the event loop while waiting for jobs

## Async Job Submission and Waiting

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run():
    ivcap = IVCAP()
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")

    # Fetch request model asynchronously
    Model = await svc.request_model_async()
    req = Model(duration_seconds=2)

    # Submit job and wait until finished
    job = await svc.request_job_async(req)
    result = await job.result_async()
    print(result)

asyncio.run(run())
```

## Async Polling Loop

When you don't want to block indefinitely, use an async polling loop:

```python
async def run():
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()
    job = await svc.request_job_async(Model(duration_seconds=5), max_wait_time=None)

    while not await job.finished_async():
        await asyncio.sleep(5)

    status = await job.status_async(refresh=False)
    print(status)
```

## Running Many Jobs in Parallel

Use `asyncio.gather()` to submit and wait for multiple jobs concurrently:

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run_job(svc, req):
    job = await svc.request_job_async(req)
    result = await job.result_async()
    return result

async def run_all():
    ivcap = IVCAP()
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()

    # Create 10 requests
    requests = [Model(duration_seconds=i) for i in range(1, 11)]

    # Submit and wait for all in parallel
    results = await asyncio.gather(*[run_job(svc, req) for req in requests])

    for i, result in enumerate(results):
        print(f"Job {i}: {result}")

asyncio.run(run_all())
```

## Async Variants Reference

| Synchronous | Async variant |
|---|---|
| `svc.request_model` | `await svc.request_model_async()` |
| `svc.request_job(req)` | `await svc.request_job_async(req)` |
| `job.refresh()` | `await job.refresh_async()` |
| `job.finished` | `await job.finished_async()` |
| `job.status()` | `await job.status_async()` |
| `job.result` | `await job.result_async()` |

## Error Handling in Async Code

```python
from ivcap_client.exception import IvcapApiError, ResourceNotFound

async def safe_run():
    try:
        svc = ivcap.get_service_by_name("my-service")
        Model = await svc.request_model_async()
        job = await svc.request_job_async(Model())
        return await job.result_async()
    except ResourceNotFound:
        print("Service not found")
    except IvcapApiError as e:
        print(f"API error [{e.status_code}]: {e}")
```

## See Also

- [Running Jobs](jobs.md) — Synchronous job patterns
- [Error Handling](error-handling.md) — Exception types and recovery
- [Examples: Async & Parallel](../examples/async-parallel.md) — Ready-to-run scripts
