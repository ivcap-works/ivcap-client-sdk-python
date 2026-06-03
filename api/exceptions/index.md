# Exceptions

All exceptions raised by the IVCAP Client SDK. Import them from
`ivcap_client.exception`.

## Quick Reference

```python
from ivcap_client.exception import (
    IvcapError,               # base class
    IvcapApiError,            # HTTP errors (.status_code, .operation)
    NotAuthorizedException,   # 401/403
    ResourceNotFound,         # 404
    AmbiguousRequest,         # multiple matches for get_service_by_name
    MissingParameterValue,    # missing required parameter
)
```

## Hierarchy

```
Exception
├── IvcapError
│   └── IvcapApiError
│       ├── NotAuthorizedException
│       └── HttpException            (backward-compat alias)
├── ResourceNotFound
├── AmbiguousRequest
└── MissingParameterValue
```

!!! note
    `ResourceNotFound`, `AmbiguousRequest`, and `MissingParameterValue` inherit
    directly from the built-in `Exception`, **not** from `IvcapError`. Catch
    `IvcapError` to handle HTTP/API errors only; use individual exception types
    (or the base `Exception`) when you also need to catch these.

## Exception Documentation

::: ivcap_client.exception
