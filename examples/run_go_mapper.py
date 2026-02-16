from pathlib import Path
from _common import create_log_file, ivcap, pp
from time import sleep, time
import csv
from ivcap_client import JobStatus

req = {
  "ids": [
    "P12345",
    "Q9H0H5"
  ],
  "category": "BP"
}

#svc = ivcap.get_service_by_name("Gene Ontology (GO) Term Mapper")
svc = ivcap.get_service("urn:ivcap:service:ac158a1f-dfb4-5dac-bf2e-9bf15e0f2cc7")
pp.pprint(svc)
req_model = svc.request_model
pp.pprint(req_model.model_json_schema())
# CHeck if request is of the right shape
passreq = req_model(**req)
pp.pprint(passreq)

job = svc.request_job(passreq)
print(f"Created job '{job.id}'")

while True:
    job.refresh()
    if job.finished:
        break
    sleep(2)

pp.pprint(job)
if job.status() == JobStatus.SUCCEEDED:
    pp.pprint(job.result)
