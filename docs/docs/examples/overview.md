# Examples Overview

The `examples/` directory contains ready-to-run Python scripts that demonstrate the
most common IVCAP Client SDK use cases.

## Setup

All examples share a common setup in `examples/_common.py`:

```python
from dotenv import load_dotenv
from ivcap_client.ivcap import IVCAP

# Load credentials from .dbg-env (or set environment variables directly)
load_dotenv('.dbg-env')
ivcap = IVCAP()
```

Create a `.dbg-env` file in the `examples/` directory:

```
IVCAP_URL=https://api.your-ivcap-deployment.net
IVCAP_JWT=<your-jwt-token>
```

Then run any example from the `examples/` directory:

```bash
cd examples/
python list_services.py
```

## Available Examples

### Service Discovery

| Script | What it demonstrates |
|---|---|
| [`list_services.py`](services.md) | List and inspect all available services with their parameters |
| [`find_service_by_name.py`](services.md) | Look up a specific service by name |

### Job Workflows

| Script | What it demonstrates |
|---|---|
| [`run_async_job.py`](jobs.md) | Async job submission using `request_job_async()` |
| [`test_failed_service.py`](jobs.md) | How to detect and handle a failed job |

### Artifacts

| Script | What it demonstrates |
|---|---|
| [`upload_artifact.py`](artifacts.md) | Upload a local file as an artifact |
| [`download_artifact.py`](artifacts.md) | Download artifact content to disk |
| [`list_artifacts.py`](artifacts.md) | Browse all artifacts with their metadata |

### Aspects & Search

| Script | What it demonstrates |
|---|---|
| [`search_aspect.py`](aspects.md) | Query the Datafabric by schema and filter |

### Async & Parallel

| Script | What it demonstrates |
|---|---|
| [`batch_stress_test.py`](async-parallel.md) | Submit many Batch-mode jobs in parallel and monitor |
| [`lambda_stress_test.py`](async-parallel.md) | Stress-test a Lambda-mode service |
| [`locus_stress_test.py`](async-parallel.md) | Parallel job submission with Locust load testing |
| [`run_crewai_agent.py`](async-parallel.md) | Run a CrewAI agent deployed on IVCAP |

## See Also

- [Getting Started: Quick Start](../getting-started/quick-start.md) — A guided walkthrough
- [Guides](../guides/overview.md) — Deep dives into each feature area
