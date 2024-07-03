import os
from _common import ivcap, pp, this_dir

artifact = ivcap.upload_artifact(
    name="test-576",
    file_path=os.path.join(this_dir, "data", "576-small.JPG"),
    policy="urn:ivcap:policy:ivcap.open.artifact"
)
pp.pprint(artifact)
