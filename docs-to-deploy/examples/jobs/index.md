# Example: Job Workflows

These examples cover submitting jobs and monitoring their execution.

## Async Job (`run_async_job.py`)

```python
from _common import ivcap, pp

req = {
    "duration_seconds": 2,
    "target_cpu_percent": 90,
    "throw_exception_at_end": False,
    "create_oom_error_at_end": False,
}

async def run():
    svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
    pp.pprint(svc)
    req_model = await svc.request_model_async()
    passreq = req_model(**req)

    # Submit job and wait for it to finish
    job = await svc.request_job_async(passreq)
    pp.pprint(job)

    # Get and print the result
    r = await job.result_async()
    pp.pprint(r)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
```

**What it demonstrates:**
- `request_model_async()` — async fetch of Pydantic schema
- `request_job_async()` — async job submission and wait
- `result_async()` — async result retrieval

## Synchronous Job with Polling

```python
import time
from _common import ivcap, pp
from ivcap_client import JobStatus

svc = ivcap.get_service_by_name("my-service")
Model = svc.request_model
job = svc.request_job(Model(param="value"))

print(f"Created job: {job.id}")

while not job.finished:
    time.sleep(5)
    job.refresh()
    print(f"Status: {job.status()}")

if job.status() == JobStatus.SUCCEEDED:
    pp.pprint(job.result)
```

## Run and Monitor with Logging

```python
import time, csv
from _common import ivcap, create_log_file

svc = ivcap.get_service("urn:ivcap:service:<uuid>")
Model = svc.request_model

jobs = [svc.request_job(Model(duration_seconds=10)) for _ in range(5)]
log = create_log_file("job-run")

with open(log, "w", newline="") as f:
    writer = csv.writer(f)
    start = time.time()
    while True:
        time.sleep(10)
        elapsed = int(time.time() - start)
        done = 0
        for j in jobs:
            j.refresh()
            writer.writerow([elapsed, j.id, j.status().value])
            if j.finished:
                done += 1
        f.flush()
        print(f"Progress: {done}/{len(jobs)}")
        if done == len(jobs):
            break
```

## See Also

- [Guide: Running Jobs](../guides/jobs.md)
- [Guide: Async Usage](../guides/async-usage.md)
- [API: Job](../api/job.md)
