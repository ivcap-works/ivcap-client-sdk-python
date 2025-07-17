from pydantic import BaseModel, Field
from _common import ivcap, pp
from time import sleep, time
import csv

from ivcap_client.job import JobStatus

class Req(BaseModel):
    duration_seconds: str = Field(60)

svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0999")
job = svc.request_job(Req())
print(job)
while True:
    sleep(10)
    job.refresh()
    status = job.status()
    print(status)
