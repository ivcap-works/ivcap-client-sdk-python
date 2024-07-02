
from _common import ivcap, pp

for i, s in enumerate(ivcap.list_services()):
    print(f"===== {i}")
    pp.pprint(s)
    for n, p in s.parameters.items():
        print(f".. {n}: {p}")
