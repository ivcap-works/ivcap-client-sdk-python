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
IvcapError
├── IvcapApiError
│   ├── NotAuthorizedException
│   └── ResourceNotFound
├── AmbiguousRequest
└── MissingParameterValue
```

## Exception Documentation

::: ivcap_client.exception
