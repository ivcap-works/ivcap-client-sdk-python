import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))
from ivcap_client.ivcap import IVCAP

import pprint
pp = pprint.PrettyPrinter(indent=2)

ivcap = IVCAP()
# how to enumerate ivcap.list_artifacts()


for i, a in enumerate(ivcap.list_artifacts()):
    print(f"=========== {i}")
    pp.pprint(a)
    for m in a.metadata:
        print(f".. {m.schema}")
    if i >= 5:
        break
