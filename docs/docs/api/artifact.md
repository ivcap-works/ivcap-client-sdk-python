# Artifact

An `Artifact` represents a binary data blob stored in IVCAP — images, CSV files,
NetCDF datasets, model checkpoints, etc. Artifacts are created by
`ivcap.upload_artifact()` or `ivcap.get_artifact()`.

## Quick Reference

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()

# Upload a file
artifact = ivcap.upload_artifact(
    name="my-data",
    file_path="/path/to/file.csv",
)
print(artifact.id, artifact.mime_type)

# Download
with artifact.as_local_file() as path:
    print(f"Downloaded to: {path}")

# Stream to disk
with open("/tmp/output.csv", "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)

# Convert (small) artifact content to a data: URL
url = artifact.as_data_url(max_length=2048)
```

## Class Documentation

::: ivcap_client.artifact.Artifact

## DataUrlArtifact

`ivcap.get_artifact()` also accepts an [RFC 2397](https://www.rfc-editor.org/rfc/rfc2397)
`data:` URL (e.g. `"data:image/png;base64,iVBORw0KGgo..."`). In that case the payload is
decoded entirely in memory and returned as a `DataUrlArtifact`, which exposes the same
`open()` / `as_stream()` / `as_local_file()` / `untar()` interface as `Artifact` — no
network or filesystem access is ever performed.

```python
artifact = ivcap.get_artifact("data:text/plain;base64,SGVsbG8h")
with artifact.open() as f:
    print(f.read())  # b"Hello!"
```

The equivalent `urn:data:...` form is also accepted, for consistency with other IVCAP
URN schemes (e.g. `urn:file://...`):

```python
artifact = ivcap.get_artifact("urn:data:text/plain;base64,SGVsbG8h")
```

::: ivcap_client.artifact.DataUrlArtifact
