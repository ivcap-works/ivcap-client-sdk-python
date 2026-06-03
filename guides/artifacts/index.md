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

### Stream to a file

```python
with open("/tmp/output.jpg", "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
```

### Open as a file-like object

```python
with artifact.open() as f:
    data = f.read()
```

### Download to a temporary file

```python
# Auto-deleted when the 'with' block exits
with artifact.as_local_file() as path:
    print(f"Downloaded to: {path}")
    # process the file here...
```

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

## Local-File Artifacts

When code runs inside IVCAP the platform provides local file paths as artifact URNs:

```python
artifact = ivcap.get_artifact("file:///data/input.csv")
# Returns a LocalFileArtifact — open()/as_local_file() work without network calls
```

## Common Patterns

### Upload data → run service → download result

```python
import io, json
ivcap = IVCAP()

# Upload input
artifact = ivcap.upload_artifact(name="input-image", file_path="/data/photo.jpg")

# Submit job
service = ivcap.get_service_by_name("my-image-processor")
job = service.request_job(io.StringIO(json.dumps({"image": artifact.id, "threshold": 0.8})))

# Wait for result
import time
while not job.finished:
    time.sleep(5)
    job.refresh()

# Download output
output = ivcap.get_artifact(job.result["output_artifact"])
with output.as_local_file() as path:
    print(f"Result saved at: {path}")
```

## See Also

- [The Datafabric & Aspects](aspects.md) — Attach metadata to artifacts
- [Running Jobs](jobs.md) — Using artifact URNs as service inputs
- [API Reference: Artifact](../api/artifact.md) — Full `Artifact` class documentation
- [Examples: Artifacts](../examples/artifacts.md) — Ready-to-run scripts
