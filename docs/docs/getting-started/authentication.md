# Authentication

The IVCAP Client SDK connects to an IVCAP deployment over HTTPS using your JWT access token.

## Getting Credentials

You need two things:

1. **IVCAP deployment URL** — the API endpoint for your IVCAP cluster
2. **JWT access token** — obtained via the `ivcap-cli`

The easiest way to get a token is via the [ivcap-cli](https://github.com/reinventingscience/ivcap-cli):

```bash
ivcap context get access-token
```

## Setting Credentials

### Environment Variables (Recommended)

Set credentials as environment variables before running your script:

```bash
export IVCAP_URL=https://api.your-ivcap-deployment.net
export IVCAP_JWT=<your-jwt-token>
export IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>   # optional
```

### `.env` File

Create a `.env` file in your project directory (never commit this to version control):

```
IVCAP_URL=https://api.your-ivcap-deployment.net
IVCAP_JWT=<your-jwt-token>
IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>
```

Then load it with `python-dotenv`:

```python
from dotenv import load_dotenv
from ivcap_client.ivcap import IVCAP

load_dotenv('.env')   # or load_dotenv('.dbg-env') as used in examples
ivcap = IVCAP()
```

### Explicit Credentials in Code

For programmatic configuration (e.g., in CI/CD pipelines):

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP(
    url="https://api.your-ivcap-deployment.net",
    token="<jwt-token>",
    account_id="urn:ivcap:account:<uuid>",  # optional
)
```

## Inside the IVCAP Platform

When code runs *inside* an IVCAP service container (as a deployed job), the platform
automatically injects `IVCAP_BASE_URL`. In this case no JWT token is needed:

```python
# IVCAP_BASE_URL is set by the platform sidecar; no token required
ivcap = IVCAP()
```

## Environment Variable Reference

| Variable | Required | Description |
|---|---|---|
| `IVCAP_URL` | Yes | Base URL for the IVCAP platform |
| `IVCAP_JWT` | Yes (external) | JWT access token |
| `IVCAP_BASE_URL` | No | Used inside platform containers (overrides `IVCAP_URL`) |
| `IVCAP_ACCOUNT_ID` | No | Your account URN (some operations require this) |

See the [full environment variable reference](../reference/environment-variables.md) for all options.

## Security Best Practices

- **Never commit** JWT tokens or `.env` files to version control
- Add `.env` and `.dbg-env` to your `.gitignore`
- JWT tokens expire — use `ivcap context get access-token` to refresh
- Use environment variables or secrets management in production pipelines

## Next Steps

- Follow the [Quick Start](quick-start.md) guide
- Learn about [Discovering Services](../guides/services.md)
