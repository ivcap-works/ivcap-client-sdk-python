# Example: Aspects & Search

These examples show how to query the Datafabric and manage typed metadata.

## Search Aspects (`search_aspect.py`)

```python
from _common import ivcap, pp

schema = 'urn:common:schema:in_collection.1'
filter = "collection~='urn:ibenthos:collection:indo_flores_0922:LB4 UQ PhotoTransect'"

for i, m in enumerate(ivcap.list_aspects(
    schema=schema,
    filter=filter,
    include_content=False,
    limit=20
)):
    print(f"=========== {i + 1}")
    pp.pprint(m)
    pp.pprint(m.aspect)
```

**What it demonstrates:**
- `ivcap.list_aspects()` with `schema` and `filter` arguments
- OData-style filter with `~=` (contains-like) operator
- `include_content=False` — returns aspect metadata only, not the JSON content
- `m.aspect` — the JSON content dict (may be `None` when `include_content=False`)

## Add Metadata to an Artifact

```python
from _common import ivcap, pp

# Get or upload an artifact
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")

# Attach custom metadata
artifact.add_metadata({
    "$schema": "urn:my-project:schema:image-annotation.1",
    "label": "coral reef",
    "confidence": 0.97,
    "annotator": "alice@csiro.au",
})

# Verify
for aspect in ivcap.list_aspects(
    entity=artifact.id,
    schema="urn:my-project:schema:image-annotation.1",
    include_content=True,
):
    pp.pprint(aspect.aspect)
```

## Add and Update an Aspect

```python
from _common import ivcap, pp

# Add a new aspect
aspect = ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my:schema:status.1",
        "status": "pending-review",
    },
)
print(f"Added aspect: {aspect.id}")

# Update (retracts old, creates new)
updated = ivcap.update_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my:schema:status.1",
        "status": "approved",
    },
)
print(f"Updated aspect: {updated.id}")
```

## List All Aspects for an Entity

```python
from _common import ivcap, pp

entity = "urn:ivcap:artifact:<uuid>"

for aspect in ivcap.list_aspects(
    entity=entity,
    include_content=True,
    order_by="valid_from",
    order_direction="ASC",
):
    print(f"[{aspect.valid_from}] {aspect.schema}")
    if aspect.aspect:
        pp.pprint(aspect.aspect)
```

## Historical Aspect Query

```python
from _common import ivcap
from datetime import datetime, timezone

# What did we know about this artifact on 2025-01-01?
past = datetime(2025, 1, 1, tzinfo=timezone.utc)
for aspect in ivcap.list_aspects(
    entity="urn:ivcap:artifact:<uuid>",
    at_time=past,
    include_content=True,
):
    print(f"Valid from {aspect.valid_from}: {aspect.schema}")
    print(aspect.aspect)
```

## Retract an Aspect

```python
from _common import ivcap

aspects = list(ivcap.list_aspects(
    entity="urn:ivcap:artifact:<uuid>",
    schema="urn:my:schema:status.1",
))
if aspects:
    aspects[0].retract()
    print(f"Retracted: {aspects[0].id}")
```

## See Also

- [Guide: The Datafabric & Aspects](../guides/aspects.md)
- [Guide: Search (Datalog)](../guides/search.md)
- [API: Aspect](../api/aspect.md)
- [API: IVCAP Client](../api/ivcap.md)
