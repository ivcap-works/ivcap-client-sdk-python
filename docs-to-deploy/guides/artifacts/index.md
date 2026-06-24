# Working with Artifacts

This guide covers uploading data, downloading results, and managing binary blobs in IVCAP.

## Overview

An **Artifact** is any binary or structured data blob consumed or produced by a job:
an image, a CSV file, a NetCDF dataset, a trained model checkpoint, etc.

An artifact has two complementary parts:

1. **Blob** — the raw bytes, stored in object storage (GCS/S3-compatible), accessed via
   TUS upload (writes) or streaming HTTP GET (reads).
2. **Aspects in the Datafabric** — typed metadata describing the artifact's MIME type,
   size, provenance (which job produced it), access policy, and any domain annotations.

> **Artifact URNs as service inputs:** When a service parameter has type `ARTIFACT`,
> you pass the artifact's URN (`urn:ivcap:artifact:<uuid>`) as the parameter value.

## Uploading Files

### Upload a local file

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

artifact = ivcap.upload_artifact(
    name="my-image",
    file_path="/path/to/image.jpg",
    policy="urn:ivcap:policy:ivcap.open.artifact",  # optional, makes it public
)
print(artifact)
# <Artifact id=urn:ivcap:artifact:<uuid>, status=ready>
```

### Upload from an in-memory stream

```python
import io

data = b"col1,col2\n1,2\n3,4\n"
artifact = ivcap.upload_artifact(
    name="my-data.csv",
    io_stream=io.BytesIO(data),
    content_type="text/csv",
    content_size=len(data),
)
```

### Upload parameters

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Human-readable name for the artifact |
| `file_path` | `str` | Local path to upload |
| `io_stream` | `IO` | In-memory stream (requires `content_type`) |
| `content_type` | `str` | MIME type (auto-detected from `file_path` extension if omitted) |
| `content_size` | `int` | Size in bytes (-1 = unknown) |
| `collection` | `URN` | Add to a named collection (`urn:ivcap:collection:...`) |
| `policy` | `URN` | Access policy (`urn:ivcap:policy:...`) |
| `chunk_size` | `int` | TUS upload chunk size (default: max) |
| `retries` | `int` | Number of retry attempts on upload failure |
| `retry_delay` | `int` | Seconds between retries |
| `force_upload` | `bool` | Re-upload even if file was previously uploaded |

## Automatic Deduplication

The SDK tracks uploads using a hidden `.ivcap-<filename>.txt` sidecar file containing
an MD5 hash of the source file. If you call `upload_artifact` again for the same
unchanged file, it returns the existing artifact immediately without re-uploading.

```python
# First call — uploads the file
artifact1 = ivcap.upload_artifact(name="data", file_path="/data/file.csv")

# Second call — returns immediately (file hasn't changed)
artifact2 = ivcap.upload_artifact(name="data", file_path="/data/file.csv")

print(artifact1.id == artifact2.id)  # True
```

Use `force_upload=True` to bypass deduplication.

### Check if a file was already uploaded

```python
artifact = ivcap.artifact_for_file("/path/to/file.jpg")
if artifact:
    print(f"Already uploaded as {artifact.id}")
else:
    artifact = ivcap.upload_artifact(name="file", file_path="/path/to/file.jpg")
```

## Getting an Artifact by URN

```python
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
print(artifact.name, artifact.size, artifact.mime_type)
```

## Downloading Artifact Content

Three methods are available, each suited to a different use case:

| Method | Best for |
|---|---|
| `as_local_file()` | **Recommended** — saves to disk with minimal code |
| `open()` | Loading small artifacts entirely into memory |
| `as_stream()` | Custom chunk processing, progress bars, piping into external APIs |

### Download to a local file (recommended)

`as_local_file()` handles all the streaming internals for you.  It supports
two patterns:

**Temporary file** (auto-deleted when the `with` block exits):

```python
with artifact.as_local_file() as path:
    print(f"Downloaded to: {path}")
    data = path.read_bytes()
# temp file is deleted here
```

**Explicit path** (file is kept):

```python
path = artifact.as_local_file("/tmp/output.jpg")
print(f"Saved to: {path}")
```

> **`LocalFileArtifact` note:** When running in local mode, `as_local_file()`
> returns a :class:`~ivcap_client.artifact.SafePath` pointing to the
> pre-existing local file.  The file is **never deleted** on context exit,
> even when used inside a `with` statement.

### Open as a file-like object (in-memory)

```python
with artifact.open() as f:
    data = f.read()           # bytes
    text = data.decode("utf-8")
```

> **Warning:** `open()` loads the entire blob into memory.  For large
> artifacts (hundreds of MB+) prefer `as_local_file()` or `as_stream()`.

### Stream in chunks (advanced)

Use `as_stream()` when you need low-level control: custom progress reporting,
piping bytes into a third-party API, or incremental processing.

```python
# Example: download with progress reporting
total = 0
with open("/tmp/output.jpg", "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
        total += len(chunk)
print(f"Downloaded {total} bytes")
```

For simply saving to disk, `as_local_file()` is more ergonomic than writing
your own chunk loop.

## Listing Artifacts

```python
for artifact in ivcap.list_artifacts(limit=20):
    print(artifact.id, artifact.name, artifact.mime_type)
    for meta in artifact.metadata:
        print(f"  schema: {meta.schema}")
```

## Artifact Provenance

Every upload and every artifact produced by a job is automatically recorded in the
Datafabric with provenance aspects:

| Aspect Schema | What it records |
|---|---|
| `urn:ivcap:schema.artifact.1` | MIME type, size, storage location |
| `urn:ivcap:schema.artifact-produced-by-order` | Link: artifact → job that created it |
| `urn:ivcap:schema.artifact-used-by-order` | Link: artifact → jobs that consumed it |

Query provenance:

```python
for aspect in ivcap.list_aspects(entity=artifact.id):
    print(aspect.schema, aspect.entity)
```

## Adding Metadata to Artifacts

```python
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
artifact.add_metadata({
    "$schema": "urn:my:schema:tag.1",
    "tags": ["marine", "coral"],
})
```

## Local Mode vs Platform Mode

IVCAP supports two distinct operating modes for working with artifacts.  The same
`upload_artifact` / `get_artifact` call-sites work in **both** modes — no `if/else`
branching in your service code is needed.

### Auto-detection (recommended)

`IVCAP()` **automatically selects the right mode** based on environment variables —
no code changes needed between local development and deployed operation:

```python
from ivcap_client import IVCAP

ivcap = IVCAP()  # LocalIVCAP locally, platform IVCAP when deployed
artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")
```

Decision logic (in order):

| Condition | Result |
|---|---|
| `IVCAP_URL` or `IVCAP_BASE_URL` env var is set | Platform `IVCAP` instance |
| `url` arg is provided | Platform `IVCAP` instance |
| `token` arg is provided (no URL) | `ValueError` — signals misconfiguration |
| None of the above | `LocalIVCAP` using `IVCAP_LOCAL_DIR` (default: `ivcap-artifacts`) |

### Platform mode

Connect to a running IVCAP deployment.  Requires `IVCAP_URL` + `IVCAP_JWT` (external
access), or `IVCAP_BASE_URL` (injected automatically when running inside a platform
container).

```python
from ivcap_client import IVCAP

# Reads credentials from environment variables
ivcap = IVCAP()
artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")
print(artifact.id)  # urn:ivcap:artifact:<uuid>
```

### Explicit local mode

Use `IVCAP.local()` (or construct `LocalIVCAP` directly) when you want to **force**
local mode regardless of environment variables — for example in unit tests:

```python
from ivcap_client import IVCAP

ivcap = IVCAP.local(base_dir="./my-artifacts")
artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")
print(artifact.id)
# urn:file:///abs/path/to/my-artifacts/result.csv
```

You can also construct `LocalIVCAP` directly:

```python
from ivcap_client import LocalIVCAP

ivcap = LocalIVCAP(base_dir="./my-artifacts")
```

The `base_dir` defaults to `ivcap-artifacts` and can be set via the
`IVCAP_LOCAL_DIR` environment variable.

#### What `LocalIVCAP` supports

**Artifacts:**

| Method | Behaviour in local mode |
|---|---|
| `upload_artifact(name, file_path, ...)` | Copies source file to `base_dir/name` |
| `upload_artifact(name, io_stream, ...)` | Writes stream bytes/text to `base_dir/name` |
| `get_artifact("file://..." or "urn:file://...")` | Returns a `LocalFileArtifact` for an existing file |
| `collection`, `policy` arguments | Accepted, silently ignored |

**Aspects** (stored as JSON files under `base_dir/aspects/`):

| Method | Behaviour in local mode |
|---|---|
| `add_aspect(entity, aspect, *, schema, policy)` | Writes a `<uuid>.json` file; returns a `LocalAspect` |
| `update_aspect(entity, aspect, *, schema, policy)` | Same as `add_aspect` (no retraction in local mode) |
| `get_aspect(aspect_id)` | Reads the JSON file by URN (`urn:ivcap:aspect:<uuid>`) or bare UUID |
| `list_aspects(entity, schema, limit)` | Scans `aspects/` directory; supports `entity`, `schema`, and `limit` filters |

```python
from ivcap_client import IVCAP, LocalAspect

ivcap = IVCAP.local(base_dir="./my-artifacts")

# Create an aspect
aspect = ivcap.add_aspect(
    entity="urn:ivcap:artifact:some-uuid",
    aspect={"$schema": "urn:my:schema:tag.1", "tags": ["marine", "coral"]},
)
print(aspect.id)    # urn:ivcap:aspect:<uuid>
print(aspect.content)

# Retrieve it later
retrieved = ivcap.get_aspect(aspect.id)
assert isinstance(retrieved, LocalAspect)
```

`LocalIVCAP` does **not** implement `list_artifacts`, `list_services`,
`list_orders`, `search`, or other methods that require a live platform
connection.  See the [Local Mode guide](local-mode.md#what-localIVCAP-supports)
for the full capability table.

#### Local-file artifact URNs

Artifacts written by `LocalIVCAP` have URNs of the form `urn:file:///absolute/path`.
These URNs can be passed back to `LocalIVCAP.get_artifact()` or to `IVCAP.get_artifact()`
(on the platform, which also supports `file://` URNs for locally-mounted inputs):

```python
artifact = ivcap.get_artifact("file:///data/input.csv")
# Returns a LocalFileArtifact — open()/as_local_file() work without network calls
```

#### Auto-naming

When `name` is omitted, `upload_artifact` generates a UUID-based filename, preserving
the source file extension if one can be inferred:

```python
artifact = ivcap.upload_artifact(file_path="/tmp/model.pkl")
print(artifact.id)
# urn:file:///abs/path/to/ivcap-artifacts/3f4a...UUID....pkl
```

## Common Patterns

### Upload data → run service → download result

```python
import io, json, time
from ivcap_client import IVCAP

ivcap = IVCAP()

# Upload input
artifact = ivcap.upload_artifact(name="input-image", file_path="/data/photo.jpg")

# Submit job
service = ivcap.get_service_by_name("my-image-processor")
job = service.request_job(io.StringIO(json.dumps({"image": artifact.id, "threshold": 0.8})))

# Wait for result
while not job.finished:
    time.sleep(5)
    job.refresh()

# Download output artifact to a temp file (auto-deleted on exit)
output = ivcap.get_artifact(job.result["output_artifact"])
with output.as_local_file() as path:
    print(f"Result saved at: {path}")
    data = path.read_bytes()

# Or keep the file at a specific path
path = output.as_local_file("/tmp/result.jpg")
print(f"Result kept at: {path}")
```

## See Also

- [The Datafabric & Aspects](aspects.md) — Attach metadata to artifacts
- [Running Jobs](jobs.md) — Using artifact URNs as service inputs
- [API Reference: Artifact](../api/artifact.md) — Full `Artifact` class documentation
- [Examples: Artifacts](../examples/artifacts.md) — Ready-to-run scripts
