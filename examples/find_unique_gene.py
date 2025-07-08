from _common import ivcap, pp
from time import sleep, time
import csv

req = {
  "set_a_species": [
    "Pseudomonas sp. SG-MS2",
    "Paraburkholderia sp. SG-MS1"
  ],
  "set_b_species": [
    "Pseudomonas putida KT2440"
  ],
  "min_seq_id": 0.6,
  "min_coverage": 0.9
}

svc = ivcap.get_service_by_name("Unique Gene Finder")
pp.pprint(svc)
req_model = svc.request_model
pp.pprint(req_model)
passreq = req_model(**req)
pp.pprint(passreq)

count = 10
jobs = []
for i in range(count):
    job = svc.request_job(passreq)
    print(f"{i:03}: Created job '{job.id}'")
    jobs.append(job)

log_file = f"exp-{int(time())}.csv"
print(f"... using log file '{job.id}'")
with open(f"exp-{int(time())}.csv", "w", newline="") as csvfile:
    w = csv.writer(csvfile)

    start_time = time()
    while True:
        sleep(10)
        et = int(time() - start_time)

        finished_count = 0
        for j in jobs:
            j.refresh()
            w.writerow([et, j.id, j.status().value])
            if j.finished:
                finished_count += 1

        csvfile.flush()
        print(f"{(et // 60):02}:{(et % 60):02} Progress: {finished_count}/{count}")
        if finished_count == count:
            break

for j in jobs:
    pp.pprint(j)

# pp.pprint(job)
# while not job.refresh().finished:
#     print("not finished, yet")
#     sleep(10)
# pp.pprint(job)

# schema = 'urn:sd-core:schema.ai-tool.1'
# for i, m in enumerate(ivcap.list_aspects(schema=schema, entity=svc.id, include_content=False, limit=2)):
#     print(f"=========== {i + 1}")
#     pp.pprint(m)
#     js = m.aspect["fn_schema"]
#     DynamicModel = model_from_json_schema(js)
#     pp.pprint(DynamicModel)
#     passreq = DynamicModel(**req)
#     pp.pprint(passreq)
#     job = svc.place_job(passreq)
#     pp.pprint(job)


# r = """
# {
#   "set_a_species": [
#     "Pseudomonas sp. SG-MS2",
#     "Paraburkholderia sp. SG-MS1"
#   ],
#   "set_b_species": [
#     "Pseudomonas putida KT2440"
#   ],
#   "min_seq_id": 0.6,
#   "min_coverage": 0.9
# }
# """
# job = svc.place_job(r)
# pp.pprint(job)
