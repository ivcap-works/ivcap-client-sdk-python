
from _common import ivcap, pp

for i, o in enumerate(ivcap.list_orders(limit=4)):
    print(f"===== {i}")
    pp.pprint(o)
    for n, p in o.parameters.items():
        print(f".. {n}: {p}")
