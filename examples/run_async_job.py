from _common import ivcap, pp
from time import sleep


req = {
    "duration_seconds": 2,
    "target_cpu_percent": 90,
    "throw_exception_at_end": True,
    "create_oom_error_at_end": False,
}

async def run():
#svc = ivcap.get_service_by_name("Batch service example")
    svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
    pp.pprint(svc)
    req_model = await svc.request_model_async()
    passreq = req_model(**req)

    job = await svc.request_job_async(passreq)
    pp.pprint(job)
    while True:
        sleep(3)
        if await job.finished_async():
            break
        pp.pprint(job)

    pp.pprint(job)
    r = await job.result_async()
    pp.pprint(r)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
