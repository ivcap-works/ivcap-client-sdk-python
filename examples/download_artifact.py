import os
from _common import ivcap, pp, this_dir

id = "urn:ivcap:artifact:8d487485-c288-459e-b4f6-7fe4c0fa41bb"
artifact = ivcap.get_artifact(id)
pp.pprint(artifact)

# ── Option 1: Download to a temporary file (auto-deleted when 'with' exits) ──
# Use this when you only need the file transiently.
with artifact.as_local_file() as path:
    print(f"Artifact content downloaded to temporary file: {path}")
    data = path.read_bytes()
    print(f"Read {len(data)} bytes")
# The temp file is automatically deleted here.

# ── Option 2: Download to a specific path (file is kept) ─────────────────────
# Use this when you want to keep the downloaded file.
output_path = f"/tmp/{artifact.name}"
path = artifact.as_local_file(output_path)
print(f"Artifact content downloaded to: {path}")

# ── Option 3: Stream in chunks (for progress reporting or custom processing) ──
# Use as_stream() when you need low-level control over the download — for
# example to report progress, pipe bytes into another API, or process data
# incrementally.  For simply saving to disk, as_local_file() above is simpler.
output_path_streamed = f"/tmp/{artifact.name}.streamed"
total = 0
with open(output_path_streamed, "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
        total += len(chunk)
print(f"Streamed {total} bytes to {output_path_streamed}")
