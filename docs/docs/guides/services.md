# Discovering Services

This guide covers how to find, inspect, and understand the IVCAP services available on your deployment.

## Overview

A **Service** is a registered, executable analytic capability. When you call
`ivcap.get_service(...)`, you are reading a `urn:ivcap:schema.service.2` aspect from
the Datafabric. Every service has a URN identifier, a name, a description, and a set
of typed parameters.

Services support multiple **execution models**, selected by the service author:

| Execution model | How it runs |
|---|---|
| **Lambda** | Long-running K8s Deployment, low-latency sequential HTTP jobs |
| **Batch** | Fresh K8s Job container per invocation, CPU/memory-intensive tasks |
| **Nextflow** | Nextflow pipeline on K8s, multi-step scientific workflows |
| **Argo** | Argo Workflow, DAG-style complex pipelines |

As a client you **do not** need to know the execution model — `service.request_job()` is
the same for all of them.

## Listing All Services

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

for i, service in enumerate(ivcap.list_services(limit=50)):
    print(f"{i}: {service}")
```

`list_services()` returns a **lazy iterator** — pages are fetched from the server
automatically as you iterate through them.

### Filtering and Ordering

```python
# Filter by name pattern
for service in ivcap.list_services(filter="name~='hello%'", limit=10):
    print(service)

# Sort by name, ascending
for service in ivcap.list_services(order_by="name", order_desc=False, limit=20):
    print(service)
```

**`list_services()` keyword arguments:**

| Argument | Type | Description |
|---|---|---|
| `limit` | `int` | Max items per page (default 10) |
| `filter` | `str` | OData-style filter, e.g. `"name~='hello%'"` |
| `order_by` | `str` | Field to sort by (e.g. `"name"`, `"created_at"`) |
| `order_desc` | `bool` | Sort descending (default `False`) |
| `at_time` | `datetime` | Return state at a historical point in time |

## Finding a Service by Name

```python
service = ivcap.get_service_by_name("hello-world-python")
print(service)
```

> **Raises:**
> - `ResourceNotFound` — if no service matches the name
> - `AmbiguousRequest` — if more than one service matches

## Getting a Service by URN

```python
service = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
```

## Inspecting Service Parameters

Each service exposes its input parameters through `service.parameters`. Each
`ServiceParameter` has a name, type, and description:

```python
service = ivcap.get_service_by_name("my-service")

# All parameters
for name, param in service.parameters.items():
    print(f"  {name}: type={param.type}, optional={param.is_optional}")

# Only mandatory parameters
print("Required:", service.mandatory_parameters)
```

**`ServiceParameter` attributes:**

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Parameter name (hyphens replaced with underscores) |
| `type` | `PType` | Enum: STRING, INT, FLOAT, BOOL, OPTION, ARTIFACT, COLLECTION |
| `description` | `str` | Human-readable description |
| `label` | `str` | UI label |
| `is_optional` | `bool` | Whether the parameter can be omitted |
| `default` | `str` | Default value (if any) |
| `options` | `list` | Allowed values for OPTION type |

## Getting the Request Model (Pydantic)

Many services expose a structured Pydantic `BaseModel` for their inputs. The SDK fetches
this from the `urn:sd-core:schema.ai-tool.1` aspect in the Datafabric and dynamically
constructs a typed class:

```python
service = ivcap.get_service("urn:ivcap:service:<uuid>")

# Access synchronously
Model = service.request_model          # type[BaseModel]
print(Model.model_json_schema())       # inspect the JSON schema

instance = Model(param_a="foo", param_b=42)
```

Or asynchronously:

```python
Model = await service.request_model_async()
```

## Common Patterns

### Discover then run

```python
service = ivcap.get_service_by_name("image-classifier")
Model = service.request_model
req = Model(image="urn:ivcap:artifact:<uuid>", threshold=0.8)
job = service.request_job(req)
```

### List all services with their parameters

```python
for service in ivcap.list_services(limit=100):
    print(f"\n=== {service.name} ({service.id}) ===")
    for name, param in service.parameters.items():
        optional = " [optional]" if param.is_optional else ""
        default = f" (default: {param.default})" if param.default else ""
        print(f"  {name}: {param.type}{optional}{default}")
        if param.description:
            print(f"    {param.description}")
```

## See Also

- [Running Jobs](jobs.md) — Submit and monitor jobs
- [API Reference: Service](../api/service.md) — Full `Service` class documentation
- [API Reference: IVCAP Client](../api/ivcap.md) — `list_services()`, `get_service()`, `get_service_by_name()`
