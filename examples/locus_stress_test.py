# Usage example:
# poetry run python locus_stress_test.py \
#     -f data/wordle.json \
#     -s urn:ivcap:service:3165bf7f-5851-5c32-bbf5-3d89c476368e \
#     -u 20 -r 10 -d 60 --max-requests 10 \
#     --host $(ivcap context get url) --token $(ivcap context get access-token --refresh-token)
import csv
import os
import argparse
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean

import json
from time import time
from gevent import sleep, spawn_later
from gevent.lock import Semaphore

from locust import HttpUser, task, events
from locust.env import Environment

from ivcap_client.ivcap import IVCAP
from ivcap_client.job import Job, JobStatus

# ---------------- In-memory capture ----------------
RESPONSES = []
RESP_LOCK = Semaphore()
MAX_BODY_BYTES = int(os.getenv("MAX_BODY_BYTES", "0"))

REQ_COUNT = 0
REQ_LOCK = Semaphore()
RUNNER = None

def analyse(recs, args):
    lat = [r["elapsed_ms"] for r in recs if r["elapsed_ms"] is not None]
    statuses = {}
    for r in recs:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1

    print("\n=== Test Summary ===")
    print(f"Host: {args.host}")
    print(f"Users: {args.users} | Spawn rate: {args.spawn_rate}/s | "
          f"Duration cap: {args.duration}s | Max requests: {args.max_requests}")
    print(f"Total requests observed: {len(recs)}")
    if lat:
        print(f"Avg latency: {round(fmean(lat), 2)} ms")
        print(f"P95 latency: {round(percentile(lat, 0.95), 2)} ms")
        print(f"P99 latency: {round(percentile(lat, 0.99), 2)} ms")
    else:
        print("No latency samples collected.")

    print("\nStatus breakdown:")
    for code in sorted(statuses.keys(), key=lambda x: (x is None, x)):
        print(f"  {code}: {statuses[code]}")

    # `recs` still holds all captured responses for further in-memory analysis.
    ivcap = IVCAP(url=args.host, token=args.token)
    service = ivcap.get_service(args.service_id)
    jobs = []
    for r in recs:
        b = r["body"]
        body = json.loads(b) if b else None
        job_id = body.get("job-id") if isinstance(body, dict) else None
        job = Job(ivcap, id=job_id, service=service).refresh() if job_id else None
        #print(job)
        jobs.append(job)
    monior_jobs(jobs, args.service_id)

def monior_jobs(jobs, log_name):
    count = len(jobs)
    with open(create_log_file(log_name), "w", newline="") as csvfile:
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

def create_log_file(name):
    log_file = Path(f"metric/{name}-{int(time())}.csv")
    print(f"... using log file '{log_file}'")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    return log_file


# ---------------- Listeners ----------------
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    global REQ_COUNT, RUNNER

    status = getattr(response, "status_code", None)
    body = ""
    location=""
    if response is not None:
        try:
            body = response.text or ""
            location = response.headers.get("Location")
        except Exception:
            body = ""
    if MAX_BODY_BYTES and len(body.encode("utf-8", "ignore")) > MAX_BODY_BYTES:
        body = body.encode("utf-8", "ignore")[:MAX_BODY_BYTES].decode("utf-8", "ignore")

    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": request_type,
        "name": name,
        "status": status,
        "elapsed_ms": round(response_time, 3) if response_time is not None else None,
        "body": body,
        "location": location,
        "error": str(exception) if exception else None,
    }
    with RESP_LOCK:
        RESPONSES.append(rec)

    with REQ_LOCK:
        REQ_COUNT += 1
        max_requests = getattr(RUNNER, "_max_requests", None)
        if max_requests is not None and REQ_COUNT >= max_requests and RUNNER and RUNNER.state != "stopped":
            RUNNER.quit()


# ---------------- User behavior ----------------
class MyUser(HttpUser):
    # Values will be injected from parsed args
    service_id = None
    host = None
    body_file = None
    token = None

    @task
    def post_request(self):
        if not hasattr(self, "_body"):
            with open(self.body_file, "r", encoding="utf-8") as f:
                self._body = f.read()

        headers = {
            "Content-Type": "application/json",
            "Timeout": "0",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        path = f"/1/services2/{self.service_id }/jobs"
        self.client.post(path, data=self._body, headers=headers, name=self.service_id)


# ---------------- Utilities ----------------
def percentile(values, p):
    if not values:
        return 0.0
    s = sorted(values)
    k = int(round((len(s) - 1) * p))
    return float(s[k])


# ---------------- Main ----------------
def main():
    global RUNNER

    parser = argparse.ArgumentParser(description="Programmatic Locust with CLI args")
    parser.add_argument("-s", "--service-id", help="Target host URL (env: IVCAP_URL)")
    parser.add_argument("-f", "--request-file", help="Path to request body file (env: BODY_FILE)")
    parser.add_argument("-u", "--users", type=int, default=10, help="Concurrent users")
    parser.add_argument("-r", "--spawn-rate", type=float, default=5.0, help="Users per second to spawn")
    parser.add_argument("-d", "--duration", type=float, default=10.0, help="Max duration in seconds")
    parser.add_argument("--max-requests", type=int, default=None,
                        help="Stop after this many requests (optional)")
    parser.add_argument("--host", default=os.getenv("IVCAP_URL", "http://localhost:8080"),
        help="Target host URL (env: IVCAP_URL)")
    parser.add_argument("--token", default=os.getenv("IVCAP_JWT"),
        help="Auth token for Authorization header (env: IVCAP_JWT)")

    args = parser.parse_args()

    # Inject into MyUser class
    MyUser.service_id = args.service_id
    MyUser.host = args.host
    MyUser.body_file = args.request_file
    MyUser.token = args.token

    env = Environment(user_classes=[MyUser])
    env.events.request.add_listener(on_request)
    RUNNER = env.create_local_runner()
    RUNNER._max_requests = args.max_requests

    RUNNER.start(user_count=args.users, spawn_rate=args.spawn_rate)

    if args.duration and args.duration > 0:
        spawn_later(args.duration, lambda: RUNNER.state != "stopped" and RUNNER.quit())

    while RUNNER.state != "stopped":
        sleep(0.2)

    recs = list(RESPONSES)
    analyse(recs, args)


if __name__ == "__main__":
    main()
