from _common import ivcap, pp

for s in ivcap.list_services(filter="name~='image-analysis-example'"):
    pp.pprint(s)
    for n, p in s.parameters.items():
        print(f".. {n}: {p}")