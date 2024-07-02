from _common import ivcap, pp

# how to enumerate ivcap.list_artifacts()
for i, a in enumerate(ivcap.list_artifacts(limit=5)):
    print(f"=========== {i}")
    pp.pprint(a)
    for m in a.metadata:
        print(f".. {m.schema}")
