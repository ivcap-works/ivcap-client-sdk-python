# IVCAP Client SDK for Python

Welcome to the **IVCAP Client SDK** — a Python library for **interacting with an
[IVCAP](https://github.com/reinventingscience/ivcap-core/) deployment from the outside** — from your laptop,
a notebook, a data pipeline, or an AI agent.

Use it to:

- ✅ **Discover and invoke services** — find registered analytic capabilities by name or URN and submit jobs to them
- ✅ **Monitor jobs** — poll status and retrieve results as jobs move through the platform
- ✅ **Manage artifacts** — upload data files and download results (images, CSV, NetCDF, …)
- ✅ **Work with the Datafabric** — read and write typed metadata (Aspects) attached to any platform entity; query provenance across the emergent knowledge graph
- ✅ **Orchestrate workflows** — chain service calls, fan out parallel jobs, and integrate IVCAP into broader data pipelines or agentic systems

> **Want to build and deploy your own analytic service on IVCAP?**
> Use the [**ivcap-service-sdk**](https://pypi.org/project/ivcap_service/) instead.
> Packaging your code as an IVCAP service lets it take full advantage of the platform's
> managed compute and storage, and makes it a reusable, discoverable building block
> that other users and agents can invoke through the same API described here.

## Quick Example

```python
from ivcap_client.ivcap import IVCAP

# Reads IVCAP_URL and IVCAP_JWT from environment variables (or a .env file)
ivcap = IVCAP()

# List available services
for service in ivcap.list_services(limit=10):
    print(service)

# Find a service by name and run a job
# request_job accepts a Pydantic BaseModel, dataclass, or IO[str] (JSON)
import io, json
service = ivcap.get_service_by_name("hello-world-python")
job = service.request_job(io.StringIO(json.dumps({"msg": "Hello, IVCAP!"})))

# Wait for the result
while not job.finished:
    import time; time.sleep(5)
    job.refresh()

print(job.result)
```

## Getting Started

New to IVCAP? Start here:

1. **[Installation](getting-started/installation.md)** — Set up the SDK
2. **[Quick Start](getting-started/quick-start.md)** — Run your first workflow in 5 minutes
3. **[Authentication](getting-started/authentication.md)** — Configure credentials

## Core Concepts

IVCAP is built around five first-class concepts:

| Concept | What it is |
|---|---|
| **Service** | A registered, executable analytic capability (Docker image + parameter schema) |
| **Job** | One invocation of a service — tracks lifecycle from `pending` → `executing` → `succeeded` |
| **Artifact** | A binary or structured data blob (image, CSV, model, …) stored in object storage |
| **Aspect** | A typed JSON assertion attached to any entity URN — forms the Datafabric knowledge graph |
| **URN** | The universal identifier for every platform entity (`urn:ivcap:service:<uuid>`, etc.) |

## Guides

- **[Discovering Services](guides/services.md)** — Find and inspect services
- **[Running Jobs](guides/jobs.md)** — Submit and monitor job execution
- **[Working with Artifacts](guides/artifacts.md)** — Upload, download, and manage data
- **[The Datafabric & Aspects](guides/aspects.md)** — Read and write typed metadata
- **[Async Usage](guides/async-usage.md)** — asyncio patterns and parallel job management
- **[Error Handling](guides/error-handling.md)** — Exception types and recovery patterns
- **[Agent Integration](guides/agents.md)** — Build AI agents that use IVCAP services

## Examples

The [`examples/`](https://github.com/ivcap-works/ivcap-client-sdk-python/tree/main/examples) directory contains ready-to-run scripts:

| Script | What it demonstrates |
|---|---|
| `list_services.py` | List and inspect all available services |
| `find_service_by_name.py` | Look up a service by name |
| `run_async_job.py` | Async job submission and monitoring |
| `upload_artifact.py` | Upload a local file as an artifact |
| `download_artifact.py` | Download artifact content |
| `search_aspect.py` | Query the Datafabric for aspects |
| `batch_stress_test.py` | Submit and monitor many parallel jobs |

See the **[Examples section](examples/overview.md)** for annotated walkthroughs.

## Where to Find Help

- **[API Reference](api/overview.md)** — Complete class and method documentation
- **[AGENTS.md](https://github.com/ivcap-works/ivcap-client-sdk-python/blob/main/AGENTS.md)** — Machine-readable quick-reference for AI agents; also available as the [Agent Guide](agent.md) doc page
- **GitHub Issues** — [Report bugs or ask questions](https://github.com/ivcap-works/ivcap-client-sdk-python/issues)
- **[Contributing](community/contributing.md)** — Contributions welcome!

## License

This project is licensed under the [BSD License](https://github.com/ivcap-works/ivcap-client-sdk-python/blob/main/LICENSE).

---

**Happy building! 🚀**
