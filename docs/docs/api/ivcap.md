# IVCAP Client

The `IVCAP` class is the single entry point for all client operations. It manages
authentication, connection, and exposes all high-level methods for working with
services, jobs, artifacts, and aspects.

## Quick Reference

```python
from ivcap_client.ivcap import IVCAP

# From environment variables (recommended)
ivcap = IVCAP()

# With explicit credentials
ivcap = IVCAP(
    url="https://api.your-ivcap-deployment.net",
    token="<jwt-token>",
    account_id="urn:ivcap:account:<uuid>",
)
```

## Class Documentation

::: ivcap_client.ivcap.IVCAP
