# Contributing

We welcome contributions to the IVCAP Client SDK!

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/ivcap-client-sdk-python.git
cd ivcap-client-sdk-python
```

### 2. Set Up Development Environment

```bash
# Install all dependencies including dev tools
poetry install --with dev
```

### 3. Create a Branch

```bash
git checkout -b feature/my-feature
```

## Development Workflow

### Running Tests

```bash
# Run all tests with coverage
poetry run pytest tests/ --cov=ivcap_client --cov-report=xml

# Run a specific test file
poetry run pytest tests/test_artifact.py -v
```

### Code Quality

```bash
# Type checking
poetry run mypy ivcap_client/
```

### Building Documentation

```bash
# Install MkDocs and mkdocstrings
pip install -r docs/requirements-docs.txt

# Serve locally (http://localhost:8000)
make docs-serve

# Build static site
make docs
```

Visit `http://localhost:8000` to preview the docs locally.

## Making Changes

### Code Changes

1. Make your changes in a feature branch
2. Add tests for new functionality in `tests/`
3. Ensure all tests pass: `poetry run pytest tests/`
4. Update documentation as needed in `docs/docs/`

### Documentation Changes

1. Edit files in `docs/docs/`
2. Test locally with `make docs-serve`
3. Check formatting and cross-links
4. Submit a pull request

### Regenerating the API Client

The `ivcap_client/api/`, `ivcap_client/models/`, and `ivcap_client/client/` directories
are auto-generated from the IVCAP OpenAPI spec. To regenerate them:

```bash
make gen
```

This requires `openapi-python-client` to be installed.

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add async variant for list_artifacts
fix: handle 404 in get_artifact gracefully
docs: update artifact guide with deduplication details
test: add tests for aspect retraction
chore: regenerate OpenAPI client from latest spec
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if behaviour changes
3. Write a clear PR description explaining what changed and why
4. Link any related issues

## Code Style

- **Type hints** — required for all public functions
- **Docstrings** — Google style, required for all public classes and methods
- **Tests** — pytest, in `tests/` directory

```python
def upload_artifact(
    self,
    name: str,
    file_path: Optional[str] = None,
    io_stream: Optional[IO] = None,
    content_type: Optional[str] = None,
) -> Artifact:
    """Upload a file or stream as an IVCAP artifact.

    Args:
        name: Human-readable name for the artifact.
        file_path: Local path to upload. MIME type auto-detected.
        io_stream: In-memory stream to upload (requires content_type).
        content_type: MIME type override.

    Returns:
        The created Artifact with its id, name, and status.

    Raises:
        IvcapApiError: If the upload fails with an HTTP error.
        ValueError: If neither file_path nor io_stream is provided.
    """
```

## Reporting Issues

### Bug Reports

Include:
- Minimal reproducible example
- Expected vs. actual behaviour
- Python version (`python --version`)
- SDK version (`python -c "import ivcap_client; print(ivcap_client.__version__)"`)
- Full traceback

### Feature Requests

Include:
- Use case and motivation
- Proposed API/syntax
- Any alternatives you've considered

## License

By contributing, you agree that your contributions will be licensed under the same
[BSD License](https://github.com/ivcap-works/ivcap-client-sdk-python/blob/main/LICENSE)
as the project.

---

Thank you for contributing to IVCAP! 🚀
