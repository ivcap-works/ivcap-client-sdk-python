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
```

## Class Documentation

::: ivcap_client.artifact.Artifact
