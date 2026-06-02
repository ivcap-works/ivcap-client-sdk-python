# Quick Start

Get a working IVCAP client workflow running in 5 minutes.

## 1. Install the SDK

```bash
pip install ivcap-client
```

## 2. Set Up Credentials

```bash
export IVCAP_URL=https://api.your-ivcap-deployment.net
export IVCAP_JWT=$(ivcap context get access-token)
```

Or use a `.env` file — see [Authentication](authentication.md) for details.

## 3. Connect and Explore Services

```python
from ivcap_client.ivcap import IVCAP

# Connect (reads IVCAP_URL and IVCAP_JWT from environment)
ivcap = IVCAP()

# List available services
for service in ivcap.list_services(limit=10):
    print(service)
```

## 4. Find a Service and Run a Job

```python
import io, json

# Find a service by name
service = ivcap.get_service_by_name("hello-world-python")
print(service)

# Inspect its parameters
for name, param in service.parameters.items():
    print(f"  {name}: type={param.type}, optional={param.is_optional}")

# Submit a job — request_job accepts a Pydantic BaseModel, a dataclass,
# or an IO[str] containing JSON (plain dicts must be wrapped):
job = service.request_job(io.StringIO(json.dumps({"msg": "Hello, IVCAP!"})))
print(f"Created job: {job.id}")
```

## 5. Wait for the Result

```python
import time

while not job.finished:
    time.sleep(5)
    job.refresh()

print("Status:", job.status())
print("Result:", job.result)
```

## 6. Upload and Use an Artifact

```python
# Upload a local file
artifact = ivcap.upload_artifact(
    name="my-data",
    file_path="/path/to/data.csv",
)
print(f"Uploaded: {artifact.id}")

# Pass the artifact URN to a service (wrap the dict in io.StringIO)
import io, json
job = service.request_job(io.StringIO(json.dumps({"input": artifact.id})))
```

## 7. Attach Metadata (Aspects)

```python
# Attach typed metadata to any entity
ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:annotation.1",
        "label": "coral reef",
        "confidence": 0.97,
    },
)
```

## What's Next

- **[Discovering Services](../guides/services.md)** — Advanced service lookup and parameter inspection
- **[Running Jobs](../guides/jobs.md)** — Timeout strategies, async patterns, batch monitoring
- **[Working with Artifacts](../guides/artifacts.md)** — Upload, download, streams, deduplication
- **[The Datafabric & Aspects](../guides/aspects.md)** — Full metadata API
- **[API Reference](../api/overview.md)** — Complete class documentation
- **[Examples](../examples/overview.md)** — Ready-to-run scripts

## Common Patterns

### Typed requests with Pydantic

Some services expose a structured Pydantic model for their inputs:

```python
service = ivcap.get_service("urn:ivcap:service:<uuid>")
Model = service.request_model        # dynamically constructed BaseModel
req = Model(duration_seconds=6, target_cpu_percent=90)
job = service.request_job(req)
```

### Async workflow

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

## Troubleshooting

### "Service not found"

```python
from ivcap_client.exception import ResourceNotFound

try:
    service = ivcap.get_service_by_name("my-service")
except ResourceNotFound:
    print("Service not found — check the name with ivcap.list_services()")
```

### JWT token expired

```bash
# Refresh your token
export IVCAP_JWT=$(ivcap context get access-token)
```
