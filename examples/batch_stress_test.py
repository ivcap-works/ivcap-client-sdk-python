from _common import create_log_file, ivcap, pp
from time import sleep, time
import csv

from ivcap_client.job import JobStatus

req = {
    "duration_seconds": 6,
    "target_cpu_percent": 90,
    "throw_exception_at_end": False,
    "create_oom_error_at_end": False,
}

#svc = ivcap.get_service_by_name("Batch service example")
svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
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

with open(create_log_file("batch-stress"), "w", newline="") as csvfile:
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
