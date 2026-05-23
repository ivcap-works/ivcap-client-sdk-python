# Aspect

An `Aspect` is a typed, time-bounded assertion attached to any entity URN in the
Datafabric. Aspects are the building blocks of IVCAP's knowledge graph.

## Quick Reference

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Add an aspect
aspect = ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:annotation.1",
        "label": "coral",
        "confidence": 0.97,
    },
)

# List aspects for an entity
for aspect in ivcap.list_aspects(entity="urn:ivcap:artifact:<uuid>"):
    print(aspect.schema, aspect.entity)
    print(aspect.aspect)   # JSON content

# Retract
aspect.retract()
```

## Class Documentation

::: ivcap_client.aspect.Aspect
