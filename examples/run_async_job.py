from _common import ivcap, pp

req = {
    "duration_seconds": 2,
    "target_cpu_percent": 90,
    "throw_exception_at_end": False,
    "create_oom_error_at_end": False,
}

async def run():
    # Can't use get_service_by_name_async because there are now multiple ones with the same name
    # svc = ivcap.get_service_by_name("Batch service example")
    svc = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
    pp.pprint(svc)
    req_model = await svc.request_model_async()
    passreq = req_model(**req)

    # Create job and wait for job to finish
    job = await svc.request_job_async(passreq)
    pp.pprint(job)
    # Get job result and print it
    r = await job.result_async()
    pp.pprint(r)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
