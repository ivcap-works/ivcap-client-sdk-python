# API Reference Overview

The API reference is automatically generated from the Python source code docstrings
using [mkdocstrings](https://mkdocstrings.github.io/). This ensures the documentation
stays in sync with the actual implementation.

## Entry Point

### [IVCAP Client](ivcap.md)

The `IVCAP` class is the single entry point for all operations. Create one instance
per application:

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()  # reads credentials from environment
```

See: [IVCAP Client](ivcap.md)

## Core Classes

### [Service](service.md)

Represents a registered IVCAP service — its metadata, parameters, and methods for
submitting jobs.

See: [Service](service.md)

### [Job](job.md)

Represents a running or completed job execution. Provides status polling, result
access, and async variants.

Also documents the `JobStatus` enum (`PENDING`, `SCHEDULED`, `EXECUTING`,
`SUCCEEDED`, `FAILED`, `ERROR`).

See: [Job](job.md)

### [Artifact](artifact.md)

Represents a binary data blob stored in IVCAP — images, CSV files, models, etc.
Provides upload, download, streaming, and metadata operations.

See: [Artifact](artifact.md)

### [Aspect](aspect.md)

Represents a typed metadata assertion attached to any platform entity. The Datafabric
is built from aspects.

See: [Aspect](aspect.md)

## Error Handling

### [Exceptions](exceptions.md)

All exception classes raised by the SDK, including:
- `IvcapError` — base class
- `IvcapApiError` — HTTP errors
- `NotAuthorizedException` — 401/403
- `ResourceNotFound` — 404
- `AmbiguousRequest` — multiple matches

See: [Exceptions](exceptions.md)

## Documentation Style

All API documentation follows Google-style docstrings:
- Clear parameter descriptions with types
- Return type documentation
- Raises section for exceptions
- Usage examples in docstrings

## Module Layout

The public API surface is:

```python
from ivcap_client.ivcap import IVCAP, URN
from ivcap_client.service import Service
from ivcap_client.job import Job, JobStatus
from ivcap_client.artifact import Artifact
from ivcap_client.aspect import Aspect
from ivcap_client.exception import (
    IvcapError, IvcapApiError, ResourceNotFound,
    AmbiguousRequest, NotAuthorizedException
)
```

The `ivcap_client.api.*`, `ivcap_client.client.*`, and `ivcap_client.models.*`
sub-packages contain auto-generated OpenAPI client code and are considered internal.
