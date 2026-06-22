# Environment Variables Reference

Complete reference of all environment variables used by the IVCAP Client SDK.

## Connection Configuration

### IVCAP_URL
- **Type**: String
- **Required**: Yes (external use)
- **Description**: Base URL for the IVCAP platform API
- **Example**: `https://api.your-ivcap-deployment.net`

### IVCAP_JWT
- **Type**: String
- **Required**: Yes (external use)
- **Description**: JWT access token for authentication
- **How to get**: `ivcap context get access-token`
- **Note**: Tokens expire — refresh as needed

### IVCAP_BASE_URL
- **Type**: String
- **Required**: Only inside platform containers
- **Description**: Injected automatically by the IVCAP platform when running inside a service container. Overrides `IVCAP_URL`. No JWT needed when this is set.
- **Example**: `http://ivcap.local`

### IVCAP_ACCOUNT_ID
- **Type**: String (URN)
- **Required**: No
- **Description**: Your account URN. Some operations (e.g., listing secrets) require this.
- **Example**: `urn:ivcap:account:a1b2c3d4-e5f6-...`

## Local Mode Configuration

### IVCAP_LOCAL_DIR
- **Type**: String (filesystem path)
- **Required**: No
- **Default**: `ivcap-artifacts`
- **Description**: Root directory for local artifact storage when running in **local mode**
  (i.e. when `IVCAP_URL` / `IVCAP_BASE_URL` are not set and `IVCAP.local()` /
  `LocalIVCAP` is used).  All artifacts written via `upload_artifact()` are stored
  under this directory.  The directory is created automatically on first use.
- **Example**: `./output/artifacts`

This variable is read by `IVCAP.local()` when no explicit `base_dir` argument is passed:

```python
# With IVCAP_LOCAL_DIR=./output/artifacts set:
ivcap = IVCAP.local()          # base_dir → ./output/artifacts
ivcap = IVCAP.local("./other") # base_dir → ./other  (explicit arg wins)
```

See the [Local Mode guide](../guides/local-mode.md) for full usage details.

## Usage

### In a `.env` / `.dbg-env` file (recommended for development)

```
IVCAP_URL=https://api.your-ivcap-deployment.net
IVCAP_JWT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>
```

Load with `python-dotenv`:

```python
from dotenv import load_dotenv
from ivcap_client.ivcap import IVCAP

load_dotenv('.dbg-env')
ivcap = IVCAP()
```

### As shell environment variables

```bash
export IVCAP_URL=https://api.your-ivcap-deployment.net
export IVCAP_JWT=$(ivcap context get access-token)
export IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>

python my_script.py
```

### In CI/CD (GitHub Actions)

```yaml
env:
  IVCAP_URL: ${{ secrets.IVCAP_URL }}
  IVCAP_JWT: ${{ secrets.IVCAP_JWT }}
```

## Variable Priority

When `IVCAP_BASE_URL` is set (inside a platform container), it takes precedence over
`IVCAP_URL`, and no JWT token is required. This allows the same code to work both
locally (with `IVCAP_URL` + `IVCAP_JWT`) and inside IVCAP (with `IVCAP_BASE_URL`).

## Security

- Never commit `.env` or `.dbg-env` files to version control
- Add them to `.gitignore`:
  ```
  .env
  .dbg-env
  *.env
  ```
- JWT tokens expire — use `ivcap context get access-token` to refresh
- In production, use a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)

## See Also

- [Authentication Guide](../getting-started/authentication.md) — Detailed setup instructions
- [ivcap-cli](https://github.com/reinventingscience/ivcap-cli) — Tool for obtaining JWT tokens
