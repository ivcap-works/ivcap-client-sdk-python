# IVCAP Client SDK Documentation

This directory contains the IVCAP Client SDK documentation, built with **MkDocs** and **mkdocstrings**.

## Quick Start

### Install dependencies

```bash
# All documentation dependencies are in pyproject.toml
# Install with poetry (recommended)
poetry install --with dev
```

### Build and serve locally

```bash
# Serve locally at http://localhost:8000 using poethepoet
poetry run poe docs-serve

# Or use the Makefile from the repo root
make docs-serve
```

Visit `http://localhost:8000` to preview the docs.

### Build the static site

```bash
# Build using poethepoet
poetry run poe docs

# Or use the Makefile from the repo root
make docs-mkdocs
```

The static site is generated in the `site/` directory.

## Structure

- **`mkdocs.yml`** — MkDocs configuration, navigation structure, plugin settings
- **`docs/`** — Source Markdown files organized by topic:
  - `index.md` — Home page
  - `getting-started/` — Installation, authentication, quick start
  - `guides/` — Feature guides (services, jobs, artifacts, aspects, async, errors, etc.)
  - `api/` — API reference (IVCAP, Service, Job, Artifact, Aspect, Exceptions)
  - `examples/` — Annotated walkthrough of example scripts
  - `reference/` — Environment variables, glossary
  - `community/` — Contributing guidelines, code of conduct
- **`site/`** — Generated static HTML (created by `poetry run poe docs`)

Note: All dependencies are defined in the root `pyproject.toml` under `[tool.poetry.group.dev.dependencies]`. Use `poetry install --with dev` to get everything needed.

## API Documentation

The API reference pages use **mkdocstrings** to auto-generate documentation from Python docstrings. Pages like `api/ivcap.md` contain:

```markdown
::: ivcap_client.ivcap.IVCAP
```

This directive pulls docstrings from the source code and renders them as formatted documentation. The docstrings must follow Google style for consistent formatting.

## Contributing

When adding documentation:

1. Write Markdown in `docs/` directory (not `.rst`)
2. Update `mkdocs.yml` to include new pages in the navigation
3. Use relative links to other docs (e.g., `../guides/jobs.md`)
4. Test locally with `mkdocs serve` before submitting a PR

See [Contributing](docs/community/contributing.md) for full guidelines.

## Deployment

The docs are deployed to GitHub Pages at https://ivcap-works.github.io/ivcap-client-sdk-python/

The `.readthedocs.yml` at the repository root may be used for automatic builds on commits.
