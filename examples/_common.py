from pathlib import Path
import sys, os
from time import time
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from ivcap_client.ivcap import IVCAP

this_dir=os.path.dirname(os.path.realpath(__file__))

import pprint
pp = pprint.PrettyPrinter(indent=2)

# Load environment variables from .env file
load_dotenv('.dbg-env')

ivcap = IVCAP()

def create_log_file(name):
    log_file = Path(f"metric/{name}-{int(time())}.csv")
    print(f"... using log file '{log_file}'")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    return log_file
