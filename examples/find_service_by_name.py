from _common import ivcap, pp

s = ivcap.get_service_by_name("Batch service example - bad")
pp.pprint(s)
for n, p in s.parameters.items():
    print(f".. {n}: {p}")

s = ivcap.get_service_by_name("unique-gene-finder")
pp.pprint(s)
for n, p in s.parameters.items():
    print(f".. {n}: {p}")

for srv in ivcap.list_services(filter="name=~g"):
   print(srv)