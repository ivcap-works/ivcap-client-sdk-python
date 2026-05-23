# ivcap-client — Python SDK for IVCAP

`ivcap-client` is a Python library for **interacting with an
[IVCAP](https://github.com/reinventingscience/ivcap-core/) (Intelligent Visual
Computing and Analytics Platform) deployment from the outside** — from your laptop,
a notebook, a data pipeline, or an AI agent.

Use it to:

- **Discover and invoke services** — find registered analytic capabilities by name or
  URN and submit jobs to them
- **Monitor jobs** — poll status and retrieve results as jobs move through the platform
- **Manage artifacts** — upload data files and download results (images, CSV, NetCDF, …)
- **Work with the Datafabric** — read and write typed metadata (Aspects) attached to any
  platform entity; query provenance across the emergent knowledge graph
- **Orchestrate workflows** — chain service calls, fan out parallel jobs, and integrate
  IVCAP into broader data pipelines or agentic systems

> **Want to build and deploy your own analytic service on IVCAP?**
> Use the [**ivcap-service-sdk**](https://pypi.org/project/ivcap_service/) instead.
> Packaging your code as an IVCAP service lets it take full advantage of the platform's
> managed compute and storage, and makes it a reusable, discoverable building block
> that other users and agents can invoke through the same API described here.

---

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Common Patterns](#common-patterns)
- [Examples](#examples)
- [Going Deeper](#going-deeper)
- [Related Projects](#related-projects)

---

## Installation

```bash
pip install ivcap-client
```

---

## Quick Start

```python
from ivcap_client.ivcap import IVCAP

# Reads IVCAP_URL and IVCAP_JWT from environment variables (or a .env file)
ivcap = IVCAP()

# List available services
for service in ivcap.list_services(limit=10):
    print(service)

# Find a service by name and run a job
service = ivcap.get_service_by_name("hello-world-python")
job = service.request_job({"msg": "Hello, IVCAP!"})

# Wait for the result
while not job.finished:
    import time; time.sleep(5)
    job.refresh()

print(job.result)
```

### Credentials

You need an IVCAP deployment URL and a JWT access token. The easiest way to get a
token is via the [ivcap-cli](https://github.com/reinventingscience/ivcap-cli):

```bash
ivcap context get access-token
```

Set your credentials as environment variables or in a `.env` file:

```
IVCAP_URL=https://api.your-ivcap-deployment.net
IVCAP_JWT=<your-jwt-token>
IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>   # optional
```

---

## Core Concepts

IVCAP is built around five first-class concepts:

| Concept | What it is |
|---|---|
| **Service** | A registered, executable analytic capability (Docker image + parameter schema) |
| **Job** | One invocation of a service — tracks lifecycle from `pending` → `executing` → `succeeded` |
| **Artifact** | A binary or structured data blob (image, CSV, model, …) stored in object storage |
| **Aspect** | A typed JSON assertion attached to any entity URN — forms the Datafabric knowledge graph |
| **URN** | The universal identifier for every platform entity (`urn:ivcap:service:<uuid>`, etc.) |

The platform supports multiple execution backends (Lambda, Batch, Nextflow, Argo) — you
don't need to know which one a service uses; the `request_job()` call is the same for all
of them.

---

## Common Patterns

### Upload data, run a service, download the result

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Upload an input artifact
artifact = ivcap.upload_artifact(name="input-image", file_path="/data/photo.jpg")

# Find the service and submit a job
service = ivcap.get_service_by_name("my-image-processor")
job = service.request_job({"image": artifact.id, "threshold": 0.8})

# Poll until done
import time
while not job.finished:
    time.sleep(5)
    job.refresh()

# Download the output artifact
output = ivcap.get_artifact(job.result["output_artifact"])
with output.as_local_file() as path:
    print(f"Result saved at: {path}")
```

### Attach metadata to any entity

```python
ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:image-annotation.1",
        "label": "coral reef",
        "confidence": 0.97,
    },
)
```

### Async usage

All major operations have `_async` variants for use with `asyncio`:

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run():
    ivcap = IVCAP()
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()
    job = await svc.request_job_async(Model(param="value"))
    result = await job.result_async()
    print(result)

asyncio.run(run())
```

---

## Examples

The [`examples/`](./examples/) directory contains ready-to-run scripts covering the most
common use cases:

| Script | What it demonstrates |
|---|---|
| [`list_services.py`](./examples/list_services.py) | List and inspect all available services |
| [`find_service_by_name.py`](./examples/find_service_by_name.py) | Look up a service by name |
| [`place_order.py`](./examples/place_order.py) | Submit a job and wait for its result |
| [`run_async_job.py`](./examples/run_async_job.py) | Async job submission and monitoring |
| [`upload_artifact.py`](./examples/upload_artifact.py) | Upload a local file as an artifact |
| [`download_artifact.py`](./examples/download_artifact.py) | Download artifact content |
| [`list_artifacts.py`](./examples/list_artifacts.py) | Browse artifacts in the platform |
| [`search_aspect.py`](./examples/search_aspect.py) | Query the Datafabric for aspects |
| [`list_orders.py`](./examples/list_orders.py) | Browse historical orders |
| [`run_crewai_agent.py`](./examples/run_crewai_agent.py) | Run a CrewAI agent via IVCAP |
| [`batch_stress_test.py`](./examples/batch_stress_test.py) | Submit and monitor many parallel jobs |
| [`lambda_stress_test.py`](./examples/lambda_stress_test.py) | Stress-test a Lambda-mode service |

All examples read credentials from a `.env` file (or environment variables). See
[`examples/_common.py`](./examples/_common.py) for the shared setup logic.

---

## Going Deeper

**[`SKILLS.md`](./SKILLS.md)** is a comprehensive reference guide — written primarily for
AI agents, but equally useful for developers who want the full picture. It covers:

- A detailed explanation of every platform concept (Services, Jobs, Artifacts, Aspects,
  URNs, the Datafabric)
- The complete end-to-end request lifecycle
- Full API reference with parameter tables for every operation
- Async patterns and parallel job management
- Error handling and all exception types
- Environment variable reference

If you want to understand *why* the API works the way it does, or need exhaustive
parameter documentation, start with `SKILLS.md`.

---

## Related Projects

| Project | Purpose |
|---|---|
| [ivcap-core](https://github.com/reinventingscience/ivcap-core/) | The IVCAP platform itself |
| [ivcap-service-sdk](https://pypi.org/project/ivcap_service/) | Build and deploy services *on* IVCAP |
| [ivcap-cli](https://github.com/reinventingscience/ivcap-cli) | Command-line tool (also the easiest way to get a JWT token) |

---

## License

See [LICENSE](./LICENSE).
