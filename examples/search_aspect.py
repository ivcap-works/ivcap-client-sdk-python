import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))
from ivcap_client import IVCAP

import pprint
pp = pprint.PrettyPrinter(indent=2)

ivcap = IVCAP()
# how to enumerate ivcap.list_artifacts()

schema = 'urn:common:schema:in_collection.1'
filter = "collection~='urn:ibenthos:collection:indo_flores_0922:LB4 UQ PhotoTransect'"
for i, m in enumerate(ivcap.list_aspect(schema=schema, filter=filter, include_content=False, limit=20)):
    print(f"=========== {i + 1}")
    pp.pprint(m)
    pp.pprint(m.aspect)
