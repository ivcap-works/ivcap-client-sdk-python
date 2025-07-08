from _common import ivcap, pp
from time import sleep, time
import csv

from ivcap_client.job import JobStatus

req = {
    "duration_seconds": 60,
    "target_cpu_percent": 90,
    "throw_exception_at_end": False
}

svc = ivcap.get_service_by_name("Batch service example")
pp.pprint(svc)
req_model = svc.request_model
pp.pprint(req_model)
passreq = req_model(**req)
pp.pprint(passreq)

count = 1
interval = 3
jobs = []
max_time = 15 + count * interval
for i in range(count):
    passreq.duration_seconds = max_time - i * interval
    job = svc.request_job(passreq)
    print(f"{i:03}: Created job '{job.id}'")
    jobs.append(job)

log_file = f"batch-stress-{int(time())}.csv"
print(f"... using log file '{log_file}'")
with open(f"exp-{int(time())}.csv", "w", newline="") as csvfile:
    w = csv.writer(csvfile)

    start_time = time()
    while True:
        sleep(10)
        et = int(time() - start_time)

        finished_count = 0
        error_count = 0
        for j in jobs:
            j.refresh()
            status = j.status()
            w.writerow([et, j.id, status.value])
            if j.finished:
                finished_count += 1
                if status != JobStatus.SUCCEEDED:
                    error_count += 1

        csvfile.flush()
        print(f"{(et // 60):02}:{(et % 60):02} Progress: {finished_count}/{error_count}/{count}")
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
