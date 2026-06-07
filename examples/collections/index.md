# Collections Examples

Ready-to-run examples demonstrating how to create, populate, and manage
IVCAP collections.

## Create and populate a collection

```python
--8<-- "examples/manage_collection.py"
```

## Minimal: create a collection and add artifacts

```python
import uuid
from ivcap_client import IVCAP

ivcap = IVCAP()

# 1. Choose a stable URN for the collection (or generate one)
coll_urn = f"urn:ivcap:collection:{uuid.uuid4()}"

# 2. Create the collection definition (idempotent — safe to call again)
coll = ivcap.create_collection(coll_urn, name="My Survey", description="…")

# 3. Add previously uploaded artifact URNs
artifact_urns = [
    "urn:ivcap:artifact:aaa",
    "urn:ivcap:artifact:bbb",
    "urn:ivcap:artifact:ccc",
]
for urn in artifact_urns:
    result = coll.add_item(urn)
    if result is None:
        print(f"  {urn} — already a member")
    else:
        print(f"  {urn} — added ({result.id})")

# 4. Iterate items
for ci in coll.items(limit=100):
    print(ci.item)
```

## Upload artifact and immediately add to a collection

```python
from ivcap_client import IVCAP

ivcap = IVCAP()

coll_urn = "urn:ivcap:collection:my-survey"

# Upload and add in one step
artifact = ivcap.upload_artifact(
    name="ctd-cast-001.nc",
    file_path="/data/ctd-cast-001.nc",
)
coll = ivcap.get_collection(coll_urn)
coll.add_item(artifact.id)
```

## List collections filtered by name

```python
from ivcap_client import IVCAP

ivcap = IVCAP()

# Exact name match
for c in ivcap.list_collections(name_filter='== "Ocean CTD Survey"'):
    print(c.urn, c.name)

# Prefix match
for c in ivcap.list_collections(name_filter='starts with "CTD"', limit=20):
    print(c.urn, c.name)

# Case-insensitive regex
for c in ivcap.list_collections(name_filter='like_regex ".*ocean.*" flag "i"'):
    print(c.urn, c.name)
```

## Remove specific items

```python
from ivcap_client import IVCAP

ivcap = IVCAP()

coll_urn = "urn:ivcap:collection:my-survey"

# Remove via Collection object
coll = ivcap.get_collection(coll_urn)
retracted = coll.remove_item("urn:ivcap:artifact:aaa")
print(retracted)  # True if removed, False if was not a member

# Remove via IVCAP method
ivcap.remove_from_collection(coll_urn, "urn:ivcap:artifact:bbb")
```

## Retract (delete) an entire collection

```python
from ivcap_client import IVCAP

ivcap = IVCAP()

coll_urn = "urn:ivcap:collection:my-survey"

# Via Collection object
coll = ivcap.get_collection(coll_urn)
total = coll.retract()
print(f"Retracted {total} aspect records")

# Or directly:
# total = ivcap.retract_collection(coll_urn)
```

## See Also

- [Guide: Collections](../guides/collections.md) — Concepts and usage patterns
- [API Reference: Collection](../api/collection.md) — Full class and function docs
- [Examples: Artifacts](artifacts.md) — Uploading data to IVCAP
