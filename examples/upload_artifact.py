import sys, os
import pprint

this_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_dir, '../src'))
from ivcap_client.ivcap import IVCAP

pp = pprint.PrettyPrinter(indent=2)

ivcap = IVCAP()
artifact = ivcap.upload_artifact(
    file_path=os.path.join(this_dir, "576.JPG"),
)
pp.pprint(artifact)
