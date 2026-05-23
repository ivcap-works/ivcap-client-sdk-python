# Example: Artifacts

These examples cover uploading, downloading, and listing artifacts.

## Upload a File (`upload_artifact.py`)

```python
import os
from _common import ivcap, pp, this_dir

artifact = ivcap.upload_artifact(
    name="test-576",
    file_path=os.path.join(this_dir, "data", "576-small.JPG"),
    policy="urn:ivcap:policy:ivcap.open.artifact"
)
pp.pprint(artifact)
```

**What it demonstrates:**
- `ivcap.upload_artifact()` with `file_path` and optional `policy`
- The SDK auto-detects MIME type from the file extension
- Returns an `Artifact` object with `id`, `name`, `mime_type`, `size`

**Expected output:**
```
Artifact(
  id='urn:ivcap:artifact:<uuid>',
  name='test-576',
  mime_type='image/jpeg',
  status='ready',
  ...
)
```

## Download an Artifact (`download_artifact.py`)

```python
from _common import ivcap, pp

# Get artifact by URN
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
pp.pprint(artifact)

# Stream to disk
output_path = "/tmp/downloaded.jpg"
with open(output_path, "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
print(f"Downloaded to: {output_path}")
```

**What it demonstrates:**
- `ivcap.get_artifact()` retrieves metadata without downloading bytes
- `artifact.as_stream()` yields chunks for streaming download

## Download to Temp File

```python
with artifact.as_local_file() as path:
    print(f"Available at: {path}")
    # use path here (e.g., open with PIL, pandas, etc.)
    import shutil
    shutil.copy(path, "/output/result.jpg")
# file is automatically deleted here
```

## List Artifacts (`list_artifacts.py`)

```python
from _common import ivcap, pp

for artifact in ivcap.list_artifacts(limit=20):
    print(f"{artifact.id}  {artifact.name}  ({artifact.mime_type})")
    for meta in artifact.metadata:
        print(f"  schema: {meta.schema}")
```

**What it demonstrates:**
- `ivcap.list_artifacts()` — lazy paginated iterator
- Each artifact exposes `.metadata` — a list of aspects describing it

## Upload from Memory

```python
import io
from _common import ivcap, pp

data = b"col1,col2\n1,2\n3,4\n5,6\n"
artifact = ivcap.upload_artifact(
    name="inline-data.csv",
    io_stream=io.BytesIO(data),
    content_type="text/csv",
    content_size=len(data),
)
pp.pprint(artifact)
```

## Check Deduplication

```python
from _common import ivcap

# Check if a file was already uploaded (without re-uploading)
existing = ivcap.artifact_for_file("/path/to/file.jpg")
if existing:
    print(f"Already uploaded: {existing.id}")
else:
    artifact = ivcap.upload_artifact(name="file", file_path="/path/to/file.jpg")
    print(f"Uploaded: {artifact.id}")
```

## See Also

- [Guide: Working with Artifacts](../guides/artifacts.md)
- [API: Artifact](../api/artifact.md)
- [API: IVCAP Client](../api/ivcap.md)
