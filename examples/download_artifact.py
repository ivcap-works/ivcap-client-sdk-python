import os
from _common import ivcap, pp, this_dir

id = "urn:ivcap:artifact:8d487485-c288-459e-b4f6-7fe4c0fa41bb"
artifact = ivcap.get_artifact(id)
pp.pprint(artifact)

# Download artifact content using streaming
output_path = f"/tmp/{artifact.name}"
with open(output_path, "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
print(f"Artifact content streamed and saved to {output_path}")
