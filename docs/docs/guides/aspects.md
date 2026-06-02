# The Datafabric & Aspects

This guide explains IVCAP's metadata system and how to read, write, and query typed
assertions (Aspects) on any platform entity.

## What is the Datafabric?

The **Datafabric** is the **single source of truth** for all platform state. It implements
an *aspect-oriented, assertion-based, provenance-preserving information store*.

Every piece of platform state — a service description, a job status update, an artifact's
MIME type, a provenance record — is stored as an **Aspect**.

## What is an Aspect?

An **Aspect** is a typed, time-bounded assertion attached to any entity URN:

```
Aspect {
  id        : urn:ivcap:aspect:<uuid>   # unique aspect record identifier
  entity    : URN                        # the entity this aspect describes
  schema    : URN                        # defines the shape/meaning of content
  content   : JSON                       # the actual information payload
  asserter  : urn:ivcap:user:<uuid>      # who asserted this information
  policy    : urn:ivcap:policy:<name>    # who can read/retract this aspect
  validFrom : timestamp                  # when this assertion became valid
  validTo   : timestamp | null           # null = "still valid"
  replaces  : urn:ivcap:aspect:<uuid>    # the prior version (for updates)
}
```

**Key rules:**

1. **Aspects are assertions.** Each is a *claim* by an `asserter` that `content` describes `entity` at `validFrom`.
2. **Aspects are never deleted.** To "update" a fact, the old aspect is *retracted* (`validTo` = now) and a new one created. The Datafabric is a complete, append-only audit log.
3. **Multiple aspects per entity are normal.** Different principals can assert different things about the same entity.
4. **Time-aware queries.** `list_aspects(at_time=T)` returns aspects valid at time T — the foundation of provenance.
5. **Aspects are valid job output.** A service can write structured results directly as Aspects without creating binary artifacts.

## Well-Known Platform Schemas

| Schema URN | What it records |
|---|---|
| `urn:ivcap:schema.service.2` | A service description |
| `urn:ivcap:schema.job.2` | Job state and metadata |
| `urn:ivcap:schema.job-result.1` | Link from a job to its result artifact |
| `urn:ivcap:schema.artifact.1` | Artifact MIME type, size, storage location |
| `urn:sd-core:schema.ai-tool.1` | Service's Pydantic/JSON input schema |

## Adding an Aspect

Attach typed metadata to any entity URN (artifact, job, or any custom URN):

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

aspect = ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:image-annotation.1",
        "label": "coral reef",
        "confidence": 0.97,
    },
)
print(aspect)
```

## Updating an Aspect

`update_aspect` retracts any previous aspect with the same `(entity, schema)` pair
before creating the new one:

```python
aspect = ivcap.update_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:image-annotation.1",
        "label": "dog",
        "confidence": 0.88,
    },
)
```

## Adding Metadata Directly to an Artifact

```python
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
artifact.add_metadata({
    "$schema": "urn:my:schema:tag.1",
    "tags": ["marine", "coral"],
})
```

## Listing and Searching Aspects

### By schema

```python
for aspect in ivcap.list_aspects(
    schema="urn:common:schema:in_collection.1",
    limit=20,
    include_content=True,
):
    print(aspect.entity, aspect.schema)
    print(aspect.aspect)           # the JSON content dict
```

### By entity

```python
for aspect in ivcap.list_aspects(entity="urn:ivcap:artifact:<uuid>"):
    print(aspect.schema)
```

### With a filter expression

```python
schema = 'urn:common:schema:in_collection.1'
filter = "collection~='urn:ibenthos:collection:indo_flores_0922'"

for aspect in ivcap.list_aspects(schema=schema, filter=filter, limit=20):
    print(aspect.entity)
```

**`list_aspects()` parameters:**

| Parameter | Description |
|---|---|
| `entity` | Filter by entity URN |
| `schema` | Filter by schema prefix (supports `%` wildcard) |
| `content_path` | JSONPath filter applied to aspect content |
| `at_time` | Historical snapshot time |
| `limit` | Max items (default 10) |
| `filter` | OData-style filter expression |
| `order_by` | Sort field (default `valid_from`) |
| `order_direction` | `"ASC"` or `"DESC"` (default `"DESC"`) |
| `include_content` | Include aspect JSON content in listing (default `True`) |

## Historical Queries

Query the exact state of any entity at any past moment:

```python
from datetime import datetime, timezone

past = datetime(2025, 1, 1, tzinfo=timezone.utc)
for aspect in ivcap.list_aspects(
    entity="urn:ivcap:artifact:<uuid>",
    at_time=past,
    include_content=True,
):
    print(f"Valid from {aspect.valid_from}: {aspect.schema}")
    print(aspect.aspect)
```

## Retracting an Aspect

Mark an aspect as no longer valid without creating a replacement:

```python
aspects = list(ivcap.list_aspects(
    entity="urn:ivcap:artifact:<uuid>",
    schema="urn:my:schema:tag.1"
))
if aspects:
    aspects[0].retract()
```

## Using Your Own Schemas

You can use any schema URN you choose — the platform does not enforce a registry.
By convention, use a namespaced URN like `urn:<project>:schema:<name>.<version>`.

```python
# Attach project-specific metadata
ivcap.add_aspect(
    entity="urn:ivcap:job:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:experiment-metadata.1",
        "experiment_id": "EXP-2025-001",
        "researcher": "alice@csiro.au",
        "parameters": {"threshold": 0.8, "model_version": "v3.2"},
    },
)
```

## See Also

- [Working with Artifacts](artifacts.md) — Attach metadata to artifact entities
- [Search (Datalog)](search.md) — Graph traversal queries over aspect data
- [API Reference: Aspect](../api/aspect.md) — Full `Aspect` class documentation
- [API Reference: IVCAP Client](../api/ivcap.md) — `add_aspect()`, `update_aspect()`, `list_aspects()`
- [Examples: Aspects & Search](../examples/aspects.md) — Ready-to-run scripts
