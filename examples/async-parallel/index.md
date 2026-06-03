# Example: Async & Parallel

These examples demonstrate running many jobs concurrently using asyncio.

## Async Single Job (`run_async_job.py`)

The simplest async pattern — submit one job and await its result:

```python
from _common import ivcap, pp

async def run():
    svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
    req_model = await svc.request_model_async()
    passreq = req_model(
        duration_seconds=2,
        target_cpu_percent=90,
        throw_exception_at_end=False,
        create_oom_error_at_end=False,
    )

    job = await svc.request_job_async(passreq)
    pp.pprint(job)

    r = await job.result_async()
    pp.pprint(r)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
```

## Batch Stress Test (`batch_stress_test.py`)

Submit many jobs to a Batch-mode service and track all of them:

```python
import asyncio
import csv
from time import time
from _common import ivcap, create_log_file

NUM_JOBS = 20
POLL_INTERVAL = 10  # seconds

async def run():
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()

    # Submit all jobs in parallel
    jobs = await asyncio.gather(*[
        svc.request_job_async(Model(duration_seconds=30))
        for _ in range(NUM_JOBS)
    ])
    print(f"Submitted {len(jobs)} jobs")

    # Monitor
    log = create_log_file("batch-stress")
    with open(log, "w", newline="") as f:
        writer = csv.writer(f)
        start = time()
        while True:
            await asyncio.sleep(POLL_INTERVAL)
            elapsed = int(time() - start)
            done = 0
            for j in jobs:
                await j.refresh_async()
                writer.writerow([elapsed, j.id, j.status().value])
                if j.finished:
                    done += 1
            f.flush()
            print(f"[{elapsed}s] Progress: {done}/{len(jobs)}")
            if done == len(jobs):
                break

    print("All jobs finished!")
    print(f"Results log: {log}")

if __name__ == "__main__":
    asyncio.run(run())
```

## Parallel Jobs with `asyncio.gather()`

The canonical pattern for running N jobs concurrently and collecting all results:

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run_one(svc, req):
    """Submit one job and return its result."""
    job = await svc.request_job_async(req)
    return await job.result_async()

async def run_all():
    ivcap = IVCAP()
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()

    requests = [Model(param=i) for i in range(10)]

    results = await asyncio.gather(*[
        run_one(svc, req) for req in requests
    ])

    for i, result in enumerate(results):
        print(f"Job {i}: {result}")

asyncio.run(run_all())
```

## Running a CrewAI Agent (`run_crewai_agent.py`)

Execute a CrewAI agent deployed as an IVCAP service:

```python
from _common import ivcap, pp

# Get the agent (same as getting a service)
agent = ivcap.get_agent("urn:ivcap:service:<uuid>")

# Get the typed request model
Model = agent.request_model

# Execute and wait for result (blocks until done)
job = agent.exec_agent(Model(
    topic="best practices for data-intensive scientific workflows",
))
pp.pprint(job.result)
```

## See Also

- [Guide: Async Usage](../guides/async-usage.md)
- [Guide: Running Jobs](../guides/jobs.md)
- [Guide: Agent Integration](../guides/agents.md)
- [API: Job](../api/job.md)
