# Service

A `Service` represents a registered, executable analytic capability on the IVCAP
platform. Services are discovered via `ivcap.list_services()`, `ivcap.get_service()`,
or `ivcap.get_service_by_name()`.

## Quick Reference

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Get a service
service = ivcap.get_service_by_name("my-service")

# Inspect parameters
for name, param in service.parameters.items():
    print(f"  {name}: {param.type}, optional={param.is_optional}")

# Get Pydantic request model
Model = service.request_model
req = Model(param_a="foo", param_b=42)

# Submit a job
job = service.request_job(req)
```

## Class Documentation

::: ivcap_client.service.Service
