# Installation

## Prerequisites

- Python 3.11 or higher
- pip or poetry package manager
- Access to an IVCAP deployment (URL and JWT token)

## From PyPI

The easiest way to install the IVCAP Client SDK:

```bash
pip install ivcap-client
```

Or with poetry:

```bash
poetry add ivcap-client
```

## From Source

For development or to use the latest unreleased features:

```bash
git clone https://github.com/ivcap-works/ivcap-client-sdk-python.git
cd ivcap-client-sdk-python
poetry install
```

## Verify Installation

Test your installation:

```bash
python -c "import ivcap_client; print(ivcap_client.__version__)"
```

You should see the version number printed.

## Optional: Development Dependencies

If you plan to contribute or build documentation locally:

```bash
# Development tools (includes Sphinx for API docs)
poetry install --with dev

# Documentation tools (MkDocs)
pip install -r docs/requirements-docs.txt
```

## Next Steps

- Set up your [authentication credentials](authentication.md)
- Follow the [Quick Start](quick-start.md) guide
- Browse the [Examples](../examples/overview.md)

## Troubleshooting

### ImportError: No module named 'ivcap_client'

Make sure you've installed the package:
```bash
pip install ivcap-client
```

If using a virtual environment, ensure it's activated.

### Python Version Error

Check your Python version:
```bash
python --version
```

The SDK requires Python 3.11+.

### Permission Denied

If you get permission errors during installation, use:
```bash
pip install --user ivcap-client
```

## Getting Help

- [Open an issue](https://github.com/ivcap-works/ivcap-client-sdk-python/issues)
- See [Contributing](../community/contributing.md)
