import os
from _common import ivcap, pp, this_dir

id = "urn:ivcap:artifact:09e0cb8c-d03f-46cd-bc20-5f269d9d0401"
artifact = ivcap.get_artifact(id)
pp.pprint(artifact)

# Download artifact content using streaming
output_path = f"/tmp/{artifact.name}"
with open(output_path, "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
print(f"Artifact content streamed and saved to {output_path}")
