# IVCAP Client SDK — Documentation

This directory contains the MkDocs Material documentation site for `ivcap-client`.

No local Python installation is required — everything runs via Docker using the official
[`squidfunk/mkdocs-material`](https://hub.docker.com/r/squidfunk/mkdocs-material) image.

---

## Table of Contents

- [Quick Start](#quick-start)
  - [Serve locally (live reload)](#serve-locally-live-reload)
  - [Build the static site](#build-the-static-site)
  - [Deploy to GitHub Pages](#deploy-to-github-pages)
- [Directory Structure](#directory-structure)
- [Runnable Examples](#runnable-examples)
- [Maintenance](#maintenance)
- [Docs Setup](#docs-setup)

---

## Quick Start

### Serve locally (live reload)

```bash
# From the project root (ivcap-client-sdk-python/) — recommended
make docs-serve

# Or manually (also from the project root):
# The whole repo is mounted at /project so that pymdownx.snippets can reach
# root-level files via base_path: [".."].
# PYTHONPATH=/project lets mkdocstrings/griffe find ivcap_client without installing it.
docker run --rm -it -p 8000:8000 \
  -v "${PWD}:/project" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  ivcap-docs serve --dev-addr=0.0.0.0:8000
```

Open [http://localhost:8000](http://localhost:8000) — pages reload automatically on save.

> **Note:** Run `make docs-image` once (or after changing `docs/requirements.txt`)
> to build the `ivcap-docs` local image before using it directly.

### Build the static site

```bash
# From the project root
make docs-build

# Or manually (from the project root):
docker run --rm \
  -v "${PWD}:/project" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  ivcap-docs build --strict
```

Output is written to `docs/site/`.

### Deploy to GitHub Pages

```bash
# From the project root
make docs-deploy

# Or manually (from the project root):
docker run --rm \
  -v "${PWD}:/project" \
  -v "${HOME}/.ssh:/root/.ssh" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  ivcap-docs gh-deploy --force
```

---

## Directory Structure

```
docs/
├── Dockerfile          # Custom Docker image (adds extra pip packages)
├── mkdocs.yml          # MkDocs configuration
├── requirements.txt    # Python deps (installed into the Docker image)
├── README.md           # This file
└── docs/               # Markdown source pages
    ├── index.md
    ├── getting-started/
    │   ├── installation.md
    │   ├── quick-start.md
    │   └── authentication.md
    ├── guides/
    │   ├── overview.md
    │   ├── services.md
    │   ├── jobs.md
    │   ├── artifacts.md
    │   ├── aspects.md
    │   ├── async-usage.md
    │   ├── error-handling.md
    │   ├── agents.md
    │   └── search.md
    ├── api/
    │   ├── overview.md
    │   ├── ivcap.md
    │   ├── service.md
    │   ├── job.md
    │   ├── artifact.md
    │   ├── aspect.md
    │   └── exceptions.md
    ├── examples/
    │   ├── overview.md
    │   ├── services.md
    │   ├── jobs.md
    │   ├── artifacts.md
    │   ├── aspects.md
    │   └── async-parallel.md
    ├── reference/
    │   ├── environment-variables.md
    │   └── glossary.md
    ├── agent.md                   # Machine-readable quick-reference (embeds root AGENTS.md via --8<--)
    ├── css/
    │   └── extra.css          # Custom overrides (see Styling section)
    ├── js/
    │   └── mermaid-init.js    # Mermaid diagram initialiser
    └── community/
        ├── contributing.md
        └── conduct.md
```

---

## Runnable Examples

The Python examples shown in the docs also live as individual runnable files
in the [`../examples/`](../examples/) directory.

```bash
# From the project root (ivcap-client-sdk-python/)
export IVCAP_URL=https://develop.ivcap.net
export IVCAP_JWT=$(ivcap context get access-token)

python examples/list_services.py
```

See [`examples/`](../examples/) for the full list.

---

## Maintenance

- [When the SDK changes](#when-the-sdk-changes)
- [Syncing the API reference pages](#syncing-the-api-reference-pages)
- [Keeping runnable examples in sync](#keeping-runnable-examples-in-sync)
- [Reviewing docs for correctness](#reviewing-docs-for-correctness)
- [Adding a new documentation page](#adding-a-new-documentation-page)
- [Removing or deprecating content](#removing-or-deprecating-content)

This section describes how to keep the documentation in sync with the library as it evolves.

### When the SDK changes

The documentation lives in `docs/docs/` and mirrors the library sources in `ivcap_client/`.
After any non-trivial change to the library, run through the checklist below.

| Library change | Docs to review / update |
|---|---|
| New resource added (`ivcap_client/<name>.py`) | Create `docs/docs/api/<name>.md`, add a guide page in `docs/docs/guides/`, add an example file in `examples/`, and register everything in `docs/mkdocs.yml` |
| Existing resource renamed or removed | Delete or rename the corresponding `docs/docs/api/<name>.md` and guide; remove references from `docs/mkdocs.yml`, `docs/docs/guides/overview.md`, `docs/docs/api/overview.md`, and the examples index |
| Method signature changed (new / removed parameters, changed return type) | Update the matching section in `docs/docs/api/<resource>.md` and any code snippets in `docs/docs/guides/<resource>.md` and `docs/docs/examples/<resource>.md` |
| New option or configuration added | Check `docs/docs/reference/environment-variables.md` and `docs/docs/getting-started/authentication.md` |
| Error types or codes changed | Update `docs/docs/api/exceptions.md` and `docs/docs/guides/error-handling.md` |
| Pagination behaviour changed | Update `docs/docs/guides/` and `docs/docs/api/` type pages |
| `IVCAP` constructor or top-level API changed | Update `docs/docs/api/ivcap.md` and `docs/docs/getting-started/quick-start.md` |
| Package name, entry-point, or export map changed | Update `docs/docs/getting-started/installation.md` and `docs/docs/index.md` |
| `AGENTS.md` at repo root changed | The `docs/docs/agent.md` page embeds root `AGENTS.md` via `--8<-- "AGENTS.md"` (pymdownx snippets). No other action needed — the docs build picks it up automatically. |

### Syncing the API reference pages

Each `docs/docs/api/<resource>.md` file documents the public methods of the corresponding
`ivcap_client/<resource>.py` module via the `mkdocstrings` directive:

```markdown
::: ivcap_client.ivcap.IVCAP
```

`mkdocstrings` uses `griffe` for static source analysis, so no local installation
is needed — it reads the source directly. A quick way to spot drift between source
and docs:

```bash
# List all public method signatures in a resource file
grep -E "^\s+def [a-z]" ivcap_client/artifact.py

# Then compare with the headings in the matching API doc page
grep "^##" docs/docs/api/artifact.md
```

Repeat for every resource file. Any method that appears in the source but not in the
docs page (or vice-versa) needs to be reconciled.

### Keeping runnable examples in sync

Every code example shown in the documentation should also exist as a standalone,
runnable Python file in the top-level `examples/` directory. The first few lines
of each example file should follow this header convention:

```python
# examples/<filename>.py
# One-line description of what this example does.
# Usage: python examples/<filename>.py [<arg1> <arg2> ...]
```

The Python files under `examples/` are the source of truth for the code snippets
embedded in the documentation. When you update an example file, copy the relevant
snippet into the matching `docs/docs/examples/<resource>.md` or guide page.

To verify all examples still compile:

```bash
# Type-check all examples without executing them
python -m py_compile examples/*.py

# Run a specific example against a real deployment
export IVCAP_URL=https://develop.ivcap.net
export IVCAP_JWT=$(ivcap context get access-token)
python examples/list_services.py
```

### Reviewing docs for correctness

To do a full review of the documentation site against the current library:

1. **Build the site and serve it locally** so you can read every page in context:

   ```bash
   make docs-image   # once, or after docs/requirements.txt changes
   make docs-serve   # opens http://localhost:8000
   ```

2. **Cross-check the API reference** — open `docs/docs/api/` and the source files
   side by side and verify that every exported class and method is accurately described.

3. **Run the examples** — run at least one example per resource area (artifacts,
   aspects, jobs, services) to confirm they still work end-to-end.

4. **Check internal links** — MkDocs will warn about broken relative links during
   build; treat all warnings as errors:

   ```bash
   make docs-build   # inspect the build output for warnings
   ```

5. **Update version references** — if the package version bumped, search for hardcoded
   version strings across the docs:

   ```bash
   grep -r "version" docs/docs/getting-started/installation.md
   ```

### Adding a new documentation page

1. Create the Markdown file in the appropriate subdirectory under `docs/docs/`.
2. Register it under the `nav:` key in `docs/mkdocs.yml`.
3. Link to it from the relevant overview page (e.g. `docs/docs/guides/overview.md`).
4. If it has runnable code, add a matching Python file under `examples/` with the
   required header, and embed it in the doc page with the `--8<--` snippet directive:
   ````markdown
   ```python
   --8<-- "examples/<filename>.py"
   ```
   ````

### Removing or deprecating content

- **Removal:** delete the Markdown file, remove the `nav:` entry in `docs/mkdocs.yml`,
  and grep for any cross-links to that page so they can be removed or redirected.
- **Deprecation:** add a `!!! warning "Deprecated"` admonition at the top of the page
  and a note explaining what to use instead.

---

## Docs Setup

- [Docker image and custom build](#docker-image-and-custom-build)
- [MkDocs configuration](#mkdocs-configuration)
- [Theme](#theme)
- [Logo](#logo)
- [Styling and custom CSS](#styling-and-custom-css)
- [Mermaid diagram support](#mermaid-diagram-support)
- [LLM-friendly output (llmstxt-md plugin)](#llm-friendly-output-llmstxt-md-plugin)
- [Markdown extensions](#markdown-extensions)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Replicating this setup elsewhere](#replicating-this-setup-elsewhere)

This section documents how the documentation site is built and configured. It is aimed
at anyone who wants to mirror this setup for a different project.

### Docker image and custom build

The base image is [`squidfunk/mkdocs-material`](https://hub.docker.com/r/squidfunk/mkdocs-material).
Because the site uses additional Python packages (extra MkDocs plugins including
`mkdocstrings` for auto-generated Python API docs), a thin custom `Dockerfile` is
provided that extends the base image:

```dockerfile
# docs/Dockerfile
FROM squidfunk/mkdocs-material
COPY requirements.txt /tmp/docs-requirements.txt
RUN pip install --no-cache-dir -r /tmp/docs-requirements.txt
```

The additional Python dependencies are listed in `docs/requirements.txt`:

```
mkdocs>=1.5.0
mkdocs-material>=9.5.0
pymdown-extensions>=10.0
mkdocs-llmstxt-md>=0.1.0
mkdocstrings[python]>=0.25.0
mkdocs-autorefs>=0.5.0
griffe>=0.45.0
```

Build the custom image once, then use it in place of the plain
`squidfunk/mkdocs-material` image:

```bash
# Build (from the docs/ directory)
docker build -t ivcap-docs .

# Serve with live reload (from the project root)
# The whole repo is mounted at /project so snippets can reach root-level files.
# PYTHONPATH=/project lets mkdocstrings/griffe find ivcap_client without installing it.
docker run --rm -it -p 8000:8000 \
  -v "${PWD}:/project" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  ivcap-docs serve --dev-addr=0.0.0.0:8000

# Build static site (from the project root)
docker run --rm \
  -v "${PWD}:/project" \
  -e PYTHONPATH=/project \
  -w /project/docs \
  ivcap-docs build --strict
```

> **Tip:** The `make docs-*` targets in the project root `Makefile` wrap these
> commands so you don't have to type them by hand.

### MkDocs configuration

All site configuration lives in `docs/mkdocs.yml`. Key top-level fields:

| Field | Value / notes |
|---|---|
| `site_name` | Human-readable title shown in the browser tab and nav header |
| `site_url` | Canonical URL of the deployed site (used for SEO and `sitemap.xml`) |
| `repo_url` | GitHub repository link; MkDocs adds an edit icon automatically |
| `edit_uri` | Path appended to `repo_url` to form per-page "Edit" links |
| `docs_dir` | Source Markdown directory (`docs/` relative to `mkdocs.yml`) |
| `site_dir` | Output directory for `mkdocs build` (`site/`) |

### Theme

The site uses the **Material for MkDocs** theme provided by the
`squidfunk/mkdocs-material` Docker image:

```yaml
theme:
  name: material
  logo: img/logo.svg
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - content.code.copy
```

Consult the [Material for MkDocs documentation](https://squidfunk.github.io/mkdocs-material/)
for the full list of available `features`, `palette` schemes, and other options.

### Logo

The site logo is an SVG file placed at:

```
docs/docs/img/logo.svg
```

It is referenced in `mkdocs.yml` as `logo: img/logo.svg` (relative to `docs_dir`).
Replace `logo.svg` with your own SVG (or PNG) and update the path in `mkdocs.yml`
accordingly.

### Styling and custom CSS

A small CSS override file at `docs/docs/css/extra.css` is loaded via:

```yaml
extra_css:
  - css/extra.css
```

Currently it styles the "Copy Markdown" button injected by the `llmstxt-md` plugin to
match the site's primary colour palette:

```css
#llms-copy-button button {
  background: var(--md-primary-fg-color) !important;
  color: var(--md-primary-bg-color) !important;
  border-radius: 4px !important;
  box-shadow: var(--md-shadow-z2) !important;
  transition: background 0.2s ease, box-shadow 0.2s ease;
}
```

Add further overrides to this file as needed; they are automatically merged by MkDocs.

### Mermaid diagram support

Diagrams are written as fenced ` ```mermaid ``` ` code blocks in Markdown.
Two pieces are required:

**1. `pymdownx.superfences` with a custom Mermaid fence** (in `mkdocs.yml`):

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

**2. Mermaid JS and a small initialisation script** (in `mkdocs.yml`):

```yaml
extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
  - js/mermaid-init.js
```

`docs/docs/js/mermaid-init.js` waits for `DOMContentLoaded`, then finds every
`<code class="language-mermaid">` element rendered by the superfences extension,
replaces it with a `<div class="mermaid">`, and calls `mermaid.run()`.

### LLM-friendly output (llmstxt-md plugin)

The [`mkdocs-llmstxt-md`](https://github.com/ivcap-works/mkdocs-llmstxt-md) plugin
generates `/llms.txt` and `/llms-full.txt` alongside the normal HTML build.
These machine-readable files allow AI tools to index the docs efficiently.

Configuration in `mkdocs.yml`:

```yaml
plugins:
  - search
  - llmstxt-md:
      enable_markdown_urls: true
      enable_llms_txt: true
      enable_llms_full: true
      markdown_description: |
        One-paragraph description of the project for AI consumers.
      sections:
        Getting Started:
          - getting-started/installation.md
          ...
```

The `extra.css` tweak described above styles the "Copy Markdown" button this plugin
adds to each page.

### Markdown extensions

The following `pymdownx` and standard MkDocs extensions are enabled:

| Extension | Purpose |
|---|---|
| `admonition` | `!!! note`, `!!! warning`, `!!! tip` callout boxes |
| `attr_list` | Add HTML attributes / CSS classes to Markdown elements |
| `def_list` | Definition lists |
| `footnotes` | Footnote references |
| `md_in_html` | Markdown content inside raw HTML blocks |
| `tables` | GitHub-flavoured Markdown tables |
| `toc` (with `permalink: true`) | Auto-generated heading anchors with ¶ links |
| `pymdownx.highlight` | Syntax highlighting with anchor line numbers |
| `pymdownx.inlinehilite` | Inline code syntax highlighting |
| `pymdownx.snippets` | Embed external file content via `--8<--` |
| `pymdownx.superfences` | Fenced code blocks + Mermaid diagrams |
| `pymdownx.tabbed` | Tabbed content blocks |

`pymdownx.snippets` is configured with `base_path: [".."]` so that snippets can
reference files one level above `docs/` (e.g. the `examples/` directory).

### GitHub Actions CI/CD

The documentation is built and deployed automatically by
`.github/workflows/docs.yml`. There are two jobs:

| Job | Trigger | What it does |
|---|---|---|
| **Build** | every push / PR to `main` | Builds the Docker image from `docs/Dockerfile`, runs `mkdocs build --strict` inside it, and uploads the generated `docs/site/` as a workflow artifact |
| **Deploy** | push to `main` only | Downloads the artifact, pushes the contents to the `gh-pages` branch, and adds a `.nojekyll` sentinel so GitHub Pages serves the raw files |

#### Why Docker in CI?

The workflow builds and runs the **same `docs/Dockerfile`** used locally. This is
intentional: it ensures that every plugin installed via `docs/requirements.txt`
(including `mkdocs-llmstxt-md` and `mkdocstrings[python]`) is available in exactly
the same environment as when you run `make docs-build` on your machine. An earlier
version of the workflow used a bare `pip install -r docs/requirements.txt` with a
plain Python runner, which produced a different theme and silently skipped plugins
that depend on the Material base image — using Docker eliminates that class of
divergence.

#### Key workflow steps

```yaml
# 1. Build the custom image (squidfunk/mkdocs-material + requirements.txt)
- name: Build docs Docker image
  run: docker build -t ivcap-docs docs/

# 2. Run mkdocs build inside the image.
#    The whole repo is mounted at /project with workdir set to /project/docs,
#    mirroring the Makefile's DOCS_DOCKER pattern so that pymdownx.snippets
#    base_path: [".."] resolves to the project root.
#    PYTHONPATH=/project lets mkdocstrings/griffe find ivcap_client without
#    installing it into the Docker image.
- name: Build documentation
  run: |
    docker run --rm \
      -v "${{ github.workspace }}:/project" \
      -e PYTHONPATH=/project \
      -w /project/docs \
      ivcap-docs build --strict
```

`--strict` promotes all MkDocs warnings (broken links, unresolved snippets, etc.)
to errors, so the build fails fast rather than producing a silently broken site.

#### Updating the workflow

The workflow file lives at `.github/workflows/docs.yml`. Common changes:

- **Pin the `squidfunk/mkdocs-material` image version** — add a `FROM` tag in
  `docs/Dockerfile` (e.g. `FROM squidfunk/mkdocs-material:9.5.49`) to prevent
  unexpected upstream changes from breaking CI.
- **Add a new plugin** — add it to `docs/requirements.txt`; it will be picked up
  automatically the next time the Docker image is built in CI.
- **Change the deploy target** — if you prefer the official
  [`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages)
  action over the manual git steps, replace the `deploy` job steps accordingly.

---

### Replicating this setup elsewhere

To copy this documentation setup to a new project:

1. **Copy the skeleton:**
   ```
   docs/Dockerfile
   docs/mkdocs.yml
   docs/requirements.txt
   docs/docs/css/extra.css
   docs/docs/js/mermaid-init.js
   docs/docs/img/logo.svg   ← replace with your own logo
   ```

2. **Edit `mkdocs.yml`:** update `site_name`, `site_url`, `repo_url`, `site_author`,
   `copyright`, and the `nav:` tree to match your project structure.

3. **Replace `docs/docs/img/logo.svg`** with your project's logo.

4. **Update `requirements.txt`** if you need different plugin versions or additional
   plugins.

5. **Build the Docker image** from the `docs/` directory:
   ```bash
   docker build -t my-project-docs .
   ```

6. **Add `make` targets** (optional but recommended) so contributors can run
   `make docs-serve`, `make docs-build`, and `make docs-deploy` without memorising
   long Docker commands.
