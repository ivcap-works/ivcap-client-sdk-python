# Collection

A `Collection` is a named, described grouping of IVCAP entity URNs (most commonly
artifacts) backed entirely by DataFabric aspects — there is no separate REST endpoint.

## Quick Reference

```python
from ivcap_client import IVCAP

ivcap = IVCAP()

# Create (or update) a collection
coll = ivcap.create_collection(
    "urn:ivcap:collection:my-survey",
    name="Ocean CTD Survey",
    description="CTD casts from voyage V2025-03",
)

# Add an item (deduplication is automatic)
item = coll.add_item("urn:ivcap:artifact:<uuid>")

# List items
for ci in coll.items(limit=50):
    print(ci.item)

# Remove a single item
coll.remove_item("urn:ivcap:artifact:<uuid>")

# Retract the entire collection
total = coll.retract()
print(f"Retracted {total} aspect records")
```

## Class Documentation

::: ivcap_client.collection.Collection

## CollectionItem

::: ivcap_client.collection.CollectionItem

## Module-Level Functions

::: ivcap_client.collection.create_collection

::: ivcap_client.collection.get_collection

::: ivcap_client.collection.list_collections

::: ivcap_client.collection.add_item_to_collection

::: ivcap_client.collection.remove_item_from_collection

::: ivcap_client.collection.retract_collection

## Schema Constants

| Constant | Value |
|---|---|
| `COLLECTION_SCHEMA` | `urn:ivcap:schema:collection.1` |
| `COLLECTION_ITEM_SCHEMA` | `urn:ivcap:schema:collection-item.1` |

## See Also

- [Guide: Collections](../guides/collections.md) — Usage patterns and examples
- [API Reference: IVCAP Client](ivcap.md) — `create_collection()`, `get_collection()`, `list_collections()`, `add_to_collection()`, `remove_from_collection()`, `retract_collection()`
- [API Reference: Aspect](aspect.md) — The underlying aspect primitives
