# Search (Datalog)

IVCAP includes a Datalog/Mangle query language for traversing the knowledge graph formed
by aspect data. This lets you run graph queries across provenance links, entity
relationships, and metadata.

## Overview

The **Search service** traverses the *emergent graph* formed by URN references embedded
in aspect content. For example:
- A job aspect references the service URN → you can find "all jobs that used service X"
- A job-result aspect references an artifact URN → you can find "all artifacts produced by jobs of service X"
- A custom aspect references other entities → you can traverse your domain graph

## Basic Usage

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Datalog query — find all JPEG artifacts
query = b"""
:- ivcap_artifact(Id, Name, MimeType),
   MimeType = "image/jpeg".
"""

results = ivcap.search(query)
for r in results.items:
    print(r)
```

## Query Language

The query language is **Mangle** (a Datalog dialect). Queries are written as Horn
clauses that the system evaluates over the aspect graph.

### Common predicates

| Predicate | Description |
|---|---|
| `ivcap_artifact(Id, Name, MimeType)` | Enumerate artifacts |
| `ivcap_job(Id, Status, ServiceId)` | Enumerate jobs |
| `ivcap_service(Id, Name)` | Enumerate services |
| `ivcap_aspect(Entity, Schema, Content)` | Enumerate aspects |

### Find artifacts by MIME type

```python
query = b"""
:- ivcap_artifact(Id, Name, MimeType),
   MimeType = "text/csv".
"""
results = ivcap.search(query)
```

### Find artifacts produced by a specific service

```python
query = b"""
:- ivcap_job(JobId, "succeeded", ServiceId),
   ServiceId = "urn:ivcap:service:<uuid>",
   ivcap_artifact_produced_by(ArtifactId, JobId).
"""
results = ivcap.search(query)
```

### Find all jobs for a service

```python
query = b"""
:- ivcap_job(JobId, Status, ServiceId),
   ServiceId = "urn:ivcap:service:<uuid>".
"""
results = ivcap.search(query)
for r in results.items:
    print(r)
```

## Result Structure

`ivcap.search()` returns a result object with an `items` list. Each item is a dict
containing the bound variables from your query.

```python
results = ivcap.search(query)
print(f"Found {len(results.items)} results")
for r in results.items:
    print(r)
```

## Relationship to Aspects

Aspects are the raw data nodes of the graph. The search service:
1. Indexes all aspect content in the Datafabric
2. Resolves URN references between aspects to build the graph
3. Evaluates Datalog rules over the graph

This means any URN you embed in an aspect's JSON content becomes a traversable edge
in the graph — enabling rich provenance queries.

## See Also

- [The Datafabric & Aspects](aspects.md) — Understanding the underlying data model
- [API Reference: IVCAP Client](../api/ivcap.md) — `search()` method
- [Examples: Aspects & Search](../examples/aspects.md) — Working search examples
