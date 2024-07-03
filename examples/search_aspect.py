from _common import ivcap, pp

schema = 'urn:common:schema:in_collection.1'
filter = "collection~='urn:ibenthos:collection:indo_flores_0922:LB4 UQ PhotoTransect'"
for i, m in enumerate(ivcap.list_aspect(schema=schema, filter=filter, include_content=False, limit=20)):
    print(f"=========== {i + 1}")
    pp.pprint(m)
    pp.pprint(m.aspect)
