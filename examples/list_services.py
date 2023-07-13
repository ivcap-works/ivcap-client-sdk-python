import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../src'))
from ivcap_client.ivcap import IVCAP
from ivcap_client.service import PType

import pprint
pp = pprint.PrettyPrinter(indent=2)

ivcap = IVCAP()

for i, s in enumerate(ivcap.list_services()):
    print(f"===== {i}")
    pp.pprint(s)
    for n, p in s.parameters.items():
        print(f".. {n}: {p}")
        # if p.type == PType.OPTION:
        #     p.verify("gpu")
        #     p.verify("bnoo")
