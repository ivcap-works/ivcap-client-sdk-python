# Example: Service Discovery

These examples show how to find and inspect IVCAP services.

## List All Services (`list_services.py`)

```python
from _common import ivcap, pp

for i, s in enumerate(ivcap.list_services(limit=50)):
    print(f"===== {i}")
    pp.pprint(s)
    for n, p in s.parameters.items():
        print(f".. {n}: {p}")
```

**What it demonstrates:**
- `ivcap.list_services()` returns a lazy iterator
- Each `Service` object prints its name, URN, and description
- `service.parameters` is a dict of `{name: ServiceParameter}`

**Run it:**

```bash
cd examples/
python list_services.py
```

## Find a Service by Name (`find_service_by_name.py`)

```python
from _common import ivcap, pp
from ivcap_client.exception import ResourceNotFound, AmbiguousRequest

service_name = "hello-world-python"

try:
    service = ivcap.get_service_by_name(service_name)
    pp.pprint(service)

    # Inspect request model
    Model = service.request_model
    print(Model.model_json_schema())

except ResourceNotFound:
    print(f"No service found with name '{service_name}'")
except AmbiguousRequest:
    print(f"Multiple services match '{service_name}' — use get_service() with a URN")
```

**What it demonstrates:**
- `get_service_by_name()` raises `ResourceNotFound` or `AmbiguousRequest`
- `service.request_model` dynamically fetches the Pydantic schema from the Datafabric

**Expected output:**
```
Service(
  id='urn:ivcap:service:<uuid>',
  name='hello-world-python',
  description='...',
  ...
)
```

## See Also

- [Guide: Discovering Services](../guides/services.md)
- [API: Service](../api/service.md)
- [API: IVCAP Client](../api/ivcap.md)
