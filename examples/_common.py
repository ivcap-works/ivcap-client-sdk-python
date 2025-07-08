import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from ivcap_client.ivcap import IVCAP

this_dir=os.path.dirname(os.path.realpath(__file__))

import pprint
pp = pprint.PrettyPrinter(indent=2)

ivcap = IVCAP()
