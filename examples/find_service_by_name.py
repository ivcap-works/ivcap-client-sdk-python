from _common import ivcap, pp

s = ivcap.get_service_by_name("Batch service example - bad")
pp.pprint(s)
for n, p in s.parameters.items():
    print(f".. {n}: {p}")
