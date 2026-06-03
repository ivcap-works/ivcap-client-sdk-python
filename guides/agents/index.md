# Agent Integration

The IVCAP Client SDK includes an `Agent` wrapper for services that follow an agent
pattern. Agents are IVCAP services designed to be invoked interactively or as part of
AI orchestration pipelines.

## What is an Agent?

An agent is a special kind of IVCAP service that wraps a conversational or
decision-making process. From the client's perspective, interacting with an agent is
similar to running a regular job — you submit a request and wait for a result.

## Getting an Agent

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Agents are services; get them by URN
agent = ivcap.get_agent("urn:ivcap:service:<uuid>")
```

## Getting the Request Model

```python
# Synchronous
Model = agent.request_model

# Asynchronous
Model = await agent.request_model_async()
```

## Executing an Agent

`exec_agent()` submits the job and polls until `job.finished`, then returns the
completed `Job`:

```python
Model = agent.request_model
job = agent.exec_agent(Model(some_param="value"))
print(job.result)
```

## Using CrewAI with IVCAP

The `examples/run_crewai_agent.py` script demonstrates how to use a CrewAI-based
agent deployed on IVCAP:

```python
from _common import ivcap, pp

# Get a CrewAI agent service
agent = ivcap.get_agent("urn:ivcap:service:<uuid>")

# Get the typed request model
Model = agent.request_model

# Execute and wait for result
job = agent.exec_agent(Model(
    topic="climate change mitigation strategies",
    max_iterations=5,
))
print(job.result)
```

## Async Agent Execution

!!! warning "Limited async support"
    `Agent` does not currently expose `request_job_async()` directly.
    To run an agent asynchronously, use `asyncio.to_thread` to call
    `exec_agent()` in a thread pool, or use the underlying service's
    async API via `agent._service.request_job_async()`:

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run():
    ivcap = IVCAP()
    agent = ivcap.get_agent("urn:ivcap:service:<uuid>")
    Model = await agent.request_model_async()

    # Option A — run the blocking exec_agent in a thread pool
    job = await asyncio.to_thread(agent.exec_agent, Model(param="value"))
    print(job.result)

    # Option B — use the underlying service's async API directly
    job = await agent._service.request_job_async(Model(param="value"))
    result = await job.result_async()
    print(result)

asyncio.run(run())
```

## See Also

- [Discovering Services](services.md) — Services and agents share the same discovery API
- [Running Jobs](jobs.md) — Job submission and monitoring patterns
- [Async Usage](async-usage.md) — Async agent patterns
- [API Reference: IVCAP Client](../api/ivcap.md) — `get_agent()` method
