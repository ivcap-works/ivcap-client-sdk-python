# AGENTS.md — ivcap-client

> **For AI coding assistants (Copilot, Cursor, Claude, Cline, …).** This file is the
> authoritative quick-reference for using the `ivcap-client` Python SDK.
> Full docs: <https://ivcap-works.github.io/ivcap-client-sdk-python/>
> Also available as [`AGENTS.md`](https://github.com/ivcap-works/ivcap-client-sdk-python/blob/main/AGENTS.md)
> at the repository root.

This document teaches AI agents how to use the `ivcap_client` Python library to interact
with an [IVCAP](https://github.com/reinventingscience/ivcap-core/) (Intelligent Visual
Computing and Analytics Platform) deployment.

> **Scope of this library:** `ivcap_client` is primarily designed for **programmatic
> interaction with the IVCAP platform from outside it** — for example, orchestrating
> workflows, integrating IVCAP into data pipelines, submitting and monitoring jobs,
> managing artifacts and metadata, or building agent tooling that calls IVCAP services.
>
> If you want to **build and deploy your own analytic service on IVCAP**, use the
> [**ivcap-service-sdk**](https://pypi.org/project/ivcap_service/) instead. Packaging
> your code as an IVCAP service lets it take full advantage of the platform's managed
> compute, memory, and storage infrastructure, and — crucially — makes it a reusable,
> discoverable building block that other users, workflows, and agents can invoke through
> the same API described in this document.

---

## Table of Contents

1. [Platform Concepts](#1-platform-concepts)
2. [Installation & Setup](#2-installation--setup)
3. [Creating an IVCAP Connection](#3-creating-an-ivcap-connection)
4. [Discovering & Inspecting Services](#4-discovering--inspecting-services)
5. [Running Jobs (Service Execution)](#5-running-jobs-service-execution)
6. [Monitoring Jobs](#6-monitoring-jobs)
7. [Artifacts — Upload & Download](#7-artifacts--upload--download)
8. [Aspects — Metadata on Any Entity](#8-aspects--metadata-on-any-entity)
9. [Secrets](#9-secrets)
10. [Agents](#10-agents)
11. [Search (Datalog)](#11-search-datalog)
12. [Error Handling](#12-error-handling)
13. [Async Usage](#13-async-usage)
14. [Environment Variable Reference](#14-environment-variable-reference)

---

## 1. Platform Concepts

Before using the API, it is essential to understand the five first-class concepts that
IVCAP is built around. Everything the platform does — data storage, computation,
provenance tracking — is expressed through this model.

```
Provider  ──registers──▶  Service  ◀──requests──  User / Agent
                               │
                          executes
                               │
                               ▼
                   ---------- Job ---------
                  ╱                        ╲
        consumes / produces        consumes / produces
                │                               │
                ▼                               ▼
            Artifact                          Aspect
      (blob in Storage +              (typed assertion in
       described by Aspects           Datafabric, attached
       in Datafabric)                  to any entity URN)
```

### 1.1 Services

A **Service** is a registered, executable analytic capability. A provider (organisation
or researcher) packages their analysis code into a Docker image, describes its input
parameters (what arguments it takes, what types they are), and publishes it to IVCAP.
Once published, any authorised user can discover and invoke it.

A service description is stored in the Datafabric under schema
`urn:ivcap:schema.service.2`. When you call `ivcap.get_service(...)`, you are reading
that aspect.

Services support multiple **execution models**, selected by the service author at
registration time:

| Execution model | How it runs | Good for |
|---|---|---|
| **Lambda** | A single long-running K8s Deployment that accepts many sequential HTTP jobs | Low-latency, lightweight tasks |
| **Batch** | A fresh K8s Job container per invocation | CPU/memory-intensive, one-shot jobs |
| **Nextflow** | A Nextflow pipeline on K8s | Multi-step scientific workflows |
| **Argo** | An Argo Workflow | DAG-style complex pipelines |

As an agent or client you do **not** need to know which execution model is in use — the
`Service.request_job()` call is the same regardless. The platform's Service Controller
selects the right dispatcher automatically.

### 1.2 Jobs

A **Job** is the tracked execution of one service invocation. When you call
`service.request_job(data)`, the platform:

1. Creates a job record (`urn:ivcap:job:<uuid>`) in the **Datafabric** with status `pending`.
2. Selects the appropriate **Dispatcher** (Lambda, Batch, Nextflow, or Argo).
3. Launches the service container alongside a **Service Sidecar** in Kubernetes.
4. The sidecar is the pod's gateway to the platform — it handles auth, artifact I/O, secret access, and result reporting on behalf of the container.
5. When the service container finishes and calls `POST /results/<jobURN>`, the sidecar writes the result as a Datafabric **Aspect** and emits completion events.
6. The platform's K8s monitor picks up those events and updates the job aspect to `succeeded / failed / error`.

**Job Lifecycle:**

```
pending → scheduled → executing → succeeded
                                → failed
                                → error
```

- `pending` — job record created, waiting for a dispatcher slot
- `scheduled` — dispatcher has provisioned the execution environment (K8s resources created)
- `executing` — service container has picked up the job and started processing
- `succeeded` — service reported success; result is available via `job.result`
- `failed` — service reported failure (business-logic failure)
- `error` — platform-level error (infrastructure, timeout, OOM, etc.)

The authoritative job state is **always the Datafabric** — the SDK reads job state
directly from it. There is no separate jobs database.

### 1.3 Artifacts

An **Artifact** is any binary or structured data blob consumed or produced by a Job:
an image, a CSV file, a NetCDF dataset, a trained model checkpoint, etc.

An artifact has two complementary parts:

1. **Blob** — the raw bytes, stored in an object store (Google Cloud Storage or
   S3-compatible). Accessed via TUS upload (writes) or streaming HTTP GET (reads).
2. **Aspects in the Datafabric** — typed metadata records describing the artifact's MIME
   type, size, provenance (which job produced it), access policy, and any
   domain-specific annotations you choose to attach.

This separation means you can query, filter, and reason about artifact metadata in the
Datafabric (e.g., "find all JPEG images produced by this service version in the last
week") without loading the actual bytes.

> **Deduplication:** The Python SDK tracks uploads using a local `.ivcap-<filename>.txt`
> sidecar file containing an MD5 hash of the source file. On a repeated `upload_artifact`
> call for the same unchanged file, the SDK returns the existing `Artifact` object
> immediately without re-uploading. Use `force_upload=True` to override.

### 1.4 The Datafabric & Aspects

The **Datafabric** is the **single source of truth** for all platform state. It
implements an *aspect-oriented, assertion-based, provenance-preserving information store*.

Every piece of platform state — a service description, a job status update, an
artifact's MIME type, a provenance record linking a job to its inputs — is stored as
an **Aspect**.

An **Aspect** is a typed, time-bounded assertion attached to any entity URN:

```
Aspect {
  id        : urn:ivcap:aspect:<uuid>   # unique aspect record identifier
  entity    : URN                        # the entity this aspect describes
  schema    : URN                        # defines the shape/meaning of content
  content   : JSON                       # the actual information payload
  asserter  : urn:ivcap:user:<uuid>      # who asserted this information
  policy    : urn:ivcap:policy:<name>    # who can read/retract this aspect
  validFrom : timestamp                  # when this assertion became valid
  validTo   : timestamp | null           # null = "still valid"
  replaces  : urn:ivcap:aspect:<uuid>    # the prior version (for logical updates)
}
```

**Critical rules to understand:**

1. **Aspects are assertions.** Each aspect is a *claim* made by an `asserter` (user,
   service, or platform component) that the `content` accurately describes the `entity`
   at `validFrom`.

2. **Aspects are never modified or deleted.** To "update" information, the old aspect is
   *retracted* (`validTo` is set to now) and a new one is created. The Datafabric is a
   **complete, append-only audit log** — every past state is always recoverable.

3. **Multiple aspects per entity are normal.** Different principals can assert different
   (possibly conflicting) things about the same entity. Multiple versions of the same
   claim are kept as a historical record.

4. **Time-aware queries.** `list_aspects(at_time=T)` returns aspects that were valid at
   time T. This is the foundation of historical provenance: "what did the platform know
   about this artifact two weeks ago?"

5. **Aspects are a valid job output.** A service does not have to produce a binary
   artifact. It can write structured results directly as Aspects in the Datafabric — for
   example, an annotation service can attach classification labels to an image artifact
   without creating a new binary blob.

6. **Aspects form a provenance graph.** Aspects can embed URN references in their JSON
   content. Over time, the complete set of aspects forms an *emergent knowledge graph*:
   artifacts linked to jobs, jobs linked to services, services linked to accounts,
   annotations linked to artifacts. The Search service (Datalog/Mangle) can traverse
   this graph.

**Well-known platform schemas:**

| Schema URN | What it records |
|---|---|
| `urn:ivcap:schema.service.2` | A service description |
| `urn:ivcap:schema.job.2` | Job state and metadata |
| `urn:ivcap:schema.job-result.1` | Link from a job to its result artifact |
| `urn:ivcap:schema.artifact.1` | Artifact MIME type, size, storage location |
| `urn:sd-core:schema.ai-tool.1` | Service's Pydantic/JSON input schema (used by `request_model`) |

**You can attach your own aspects** using any schema URN you choose. This is how you
add domain-specific metadata to any entity — artifact, job, or any custom entity URN.

### 1.5 URNs — Universal Identifiers

Every entity in IVCAP is identified by a **URN** — a globally unique, typeless
identifier. Information *about* an entity is carried exclusively by its aspects.

| Entity type | URN pattern |
|---|---|
| Service | `urn:ivcap:service:<uuid>` |
| Job | `urn:ivcap:job:<uuid>` |
| Artifact | `urn:ivcap:artifact:<uuid>` |
| Aspect | `urn:ivcap:aspect:<uuid>` |
| Account | `urn:ivcap:account:<uuid>` |
| Policy | `urn:ivcap:policy:<name>` |
| Schema | `urn:ivcap:schema.<name>.<version>` |
| Queue | `urn:ivcap:queue:<uuid>` |
| User | `urn:ivcap:user:<uuid>` |

When you see a string like `"urn:ivcap:service:3678e5f1-..."` in code or API
responses, you are looking at the canonical identifier for a platform entity.

### 1.6 End-to-End Flow Summary

```
1. You call service.request_job(data)
      │
      ▼
2. API Gateway authenticates your JWT and authorises the request
      │
      ▼
3. Service Controller loads the service from Datafabric,
   creates a job record (status: pending), selects a Dispatcher
      │
      ▼
4. Dispatcher launches the execution environment (K8s Job / Deployment)
   and updates job to "scheduled"
      │
      ▼
5. Service Sidecar fetches the job; service container starts processing
   → job status becomes "executing"
      │
      ▼
6. Service reads input Artifacts/Aspects, runs analysis
      │
      ▼
7. Service writes results back via the sidecar:
   - New Artifacts uploaded to Storage
   - Result Aspects written to Datafabric
   → job status becomes "succeeded" or "failed" / "error"
      │
      ▼
8. You call job.refresh() / job.result to retrieve the outcome
```

---

## 2. Installation & Setup

```bash
pip install ivcap-client
```

The library requires an IVCAP deployment URL and a JWT access token. The easiest way
to get a token is via the [ivcap-cli](https://github.com/reinventingscience/ivcap-cli):

```bash
ivcap context get access-token
```

Store credentials in a `.env` file (loaded via `python-dotenv`) or set them as
environment variables before running your script:

```
IVCAP_URL=https://api.your-ivcap-deployment.net
IVCAP_JWT=<your-jwt-token>
IVCAP_ACCOUNT_ID=urn:ivcap:account:<uuid>
```

---

## 3. Creating an IVCAP Connection

The `IVCAP` class is the single entry point for all operations.  The same
`ivcap = IVCAP()` line works in every environment — the right implementation is
selected automatically from environment variables.

### The three operating modes at a glance

| Mode | When to use | ENV vars needed |
|---|---|---|
| **Platform (external)** | Apps, scripts, notebooks, and AI agents that access a live platform deployment over HTTPS — the primary use case for this library | `IVCAP_URL` + `IVCAP_JWT` |
| **Platform (in-container)** | Service code that runs *inside* an IVCAP job container — the sidecar handles auth transparently | `IVCAP_BASE_URL` (injected by platform) |
| **Local** | Developing and testing a service locally before deployment to IVCAP — reads/writes the local filesystem, no network calls | *(none)* |

> **Scope of the two use cases:**
> - **Mode 1 (external platform)** is the bread-and-butter of this library: write scripts
>   and applications that submit jobs, manage data, and query the Datafabric on a running
>   IVCAP deployment.
> - **Mode 3 (local)** is for service developers who want to exercise their service code
>   locally with real input files before deploying to the platform.

### Mode 1 — Platform (External Access)

Connect to a running IVCAP deployment with a JWT token:

```python
from dotenv import load_dotenv
from ivcap_client import IVCAP

load_dotenv(".dbg-env")  # loads IVCAP_URL and IVCAP_JWT from a local file
ivcap = IVCAP()          # → full platform IVCAP instance

for svc in ivcap.list_services(limit=10):
    print(svc)
```

With explicit credentials:

```python
ivcap = IVCAP(
    url="https://api.your-ivcap-deployment.net",
    token="<jwt-token>",
    account_id="urn:ivcap:account:<uuid>",  # optional
)
```

### Mode 2 — Platform (Inside a Container)

When a service runs *inside* IVCAP the platform injects `IVCAP_BASE_URL`. No JWT
token is needed — the Service Sidecar handles authentication on behalf of the container:

```python
# IVCAP_BASE_URL is set by the platform; no token required
ivcap = IVCAP()
```

### Mode 3 — Local Mode (No Platform Required)

When neither `IVCAP_URL` nor `IVCAP_BASE_URL` is set and no explicit `token` is
passed, `IVCAP()` **automatically returns a `LocalIVCAP` instance** — a
filesystem-backed *subclass* of `IVCAP` that stores artifacts and aspects under a
local directory.  No network calls are made.

This mode is primarily for **testing a service locally before deployment**: run your
service code against real input files, inspect the outputs under `ivcap-artifacts/`,
and only deploy to the platform once everything looks correct.

```python
from ivcap_client import IVCAP, LocalIVCAP

ivcap = IVCAP()  # → LocalIVCAP when no URL env var is set
artifact = ivcap.upload_artifact(name="result.csv", file_path="/tmp/result.csv")
print(artifact.id)  # urn:file:///abs/path/to/ivcap-artifacts/artifacts/result.csv
```

**Auto-detection decision (in order):**

| Condition | Result |
|---|---|
| `IVCAP_URL` or `IVCAP_BASE_URL` env var is set | Platform `IVCAP` instance |
| `url` argument is provided | Platform `IVCAP` instance |
| `token` argument provided without a URL | `ValueError` — signals misconfiguration |
| None of the above | `LocalIVCAP` using `IVCAP_LOCAL_DIR` (default: `ivcap-artifacts`) |

**Force local mode explicitly** (useful in tests):

```python
ivcap = IVCAP.local(base_dir="./my-artifacts")  # always LocalIVCAP
# or directly:
from ivcap_client import LocalIVCAP
ivcap = LocalIVCAP(base_dir="./my-artifacts")
```

**Detect which mode is active at runtime:**

```python
if isinstance(ivcap, LocalIVCAP):
    print("Local mode — artifacts at:", ivcap.base_dir)
else:
    print("Platform mode — connected to:", ivcap.url)
```

> **`LocalIVCAP` is a subclass of `IVCAP`** — it overrides only the methods that
> differ in local mode.  The directory layout under `base_dir` is:
>
> ```
> <base_dir>/
>   artifacts/   ← artifact files written by upload_artifact
>   aspects/     ← aspect JSON files written by add_aspect / update_aspect
> ```
>
> Supported operations:
>
> | Operation | Supported locally? |
> |---|---|
> | `upload_artifact`, `get_artifact` | ✓ |
> | `add_aspect`, `update_aspect`, `get_aspect` | ✓ |
> | `list_aspects(entity, schema, limit)` | ✓ (filesystem scan) |
> | `list_services`, `list_orders`, `list_artifacts` | ✗ (platform-only) |
> | `search`, `create_collection`, `list_secrets` | ✗ (platform-only) |
>
> See the full [Local Mode guide](https://ivcap-works.github.io/ivcap-client-sdk-python/guides/local-mode/)
> for detailed examples and configuration.

### Common pattern in examples

```python
from dotenv import load_dotenv
from ivcap_client.ivcap import IVCAP

load_dotenv('.dbg-env')  # loads IVCAP_URL and IVCAP_JWT from a local file
ivcap = IVCAP()
```

---

## 4. Discovering & Inspecting Services

### List all services

```python
for i, service in enumerate(ivcap.list_services(limit=50)):
    print(f"{i}: {service}")
    for name, param in service.parameters.items():
        print(f"  {name}: {param}")
```

`list_services()` returns a lazy iterator — pages are fetched automatically as you iterate.

> **Under the hood:** each `Service` object is backed by a `urn:ivcap:schema.service.2`
> aspect in the Datafabric. Calling `service.parameters` or `service.request_model`
> triggers a live read from the Datafabric if the data is not already cached locally.

**Keyword arguments:**

| Argument | Type | Description |
|---|---|---|
| `limit` | `int` | Max items per page (default 10) |
| `filter` | `str` | OData-style filter, e.g. `"name~='hello%'"` |
| `order_by` | `str` | Field to sort by |
| `order_desc` | `bool` | Sort descending (default False) |
| `at_time` | `datetime` | Return state at a historical point in time |

### Find a service by name

```python
service = ivcap.get_service_by_name("hello-world-python")
print(service)
# Raises ResourceNotFound if no match, AmbiguousRequest if multiple matches
```

### Get a service by URN

```python
service = ivcap.get_service("urn:ivcap:service:3678e5f1-8fb7-5ad6-b65b-8bd8c23c0948")
```

### Inspect service parameters

```python
service = ivcap.get_service_by_name("my-service")

# All parameters
for name, param in service.parameters.items():
    print(f"  {name}: type={param.type}, optional={param.is_optional}")

# Only mandatory parameters
print("Required:", service.mandatory_parameters)
```

Each `ServiceParameter` has:

| Attribute | Type | Description |
|---|---|---|
| `name` | `str` | Parameter name (hyphens replaced with underscores) |
| `type` | `PType` | Enum: STRING, INT, FLOAT, BOOL, OPTION, ARTIFACT, COLLECTION |
| `description` | `str` | Human-readable description |
| `label` | `str` | UI label |
| `is_optional` | `bool` | Whether the parameter can be omitted |
| `default` | `str` | Default value (if any) |
| `options` | `list` | Allowed values for OPTION type |

### Get the request model (Pydantic schema)

Many services expose a structured Pydantic model describing their input. This model is
stored as a `urn:sd-core:schema.ai-tool.1` aspect attached to the service entity in the
Datafabric. The SDK fetches it and dynamically constructs a Pydantic `BaseModel` class:

```python
service = ivcap.get_service("urn:ivcap:service:<uuid>")
Model = service.request_model          # type[BaseModel]
print(Model.model_json_schema())       # inspect the JSON schema

instance = Model(param_a="foo", param_b=42)
```

---

## 5. Running Jobs (Service Execution)

A *job* is created by submitting a request to a service. The request payload (JSON) is
forwarded to the appropriate dispatcher (Lambda, Batch, Nextflow, or Argo) which
launches the service container in Kubernetes. Input data can be a Pydantic `BaseModel`
instance, a Python dataclass, or a JSON `IO` stream.

> **How `timeout` works:** The IVCAP API Gateway passes a `Timeout` header to the
> Service Controller. If `timeout=0`, the gateway returns `202 Accepted` immediately
> with a job ID (async pattern). If `timeout > 0`, the gateway holds the HTTP connection
> open and returns `200 OK` with the result inline when the job finishes within that
> window. If the job hasn't finished by the timeout, you get a `202` and must poll.
> Use `job.refresh()` and `job.finished` for the polling pattern.

### Synchronous fire-and-check

```python
from ivcap_client.ivcap import IVCAP

ivcap = IVCAP()
svc = ivcap.get_service("urn:ivcap:service:<uuid>")

# Build the request
Model = svc.request_model
req = Model(duration_seconds=6, target_cpu_percent=90)

# Submit — returns immediately (timeout=0 means "don't wait")
job = svc.request_job(req)
print(f"Created job '{job.id}'")
```

### Synchronous wait for completion (blocking)

Pass `timeout` in seconds; the service gateway will block until done or the timeout
elapses. Use `timeout=None` to wait indefinitely:

```python
job = svc.request_job(req, timeout=120)   # block up to 120 s server-side
```

> **Note:** `timeout=0` means "submit and return immediately with a 202 Accepted".
> Use `job.refresh()` / `job.finished` to poll progress.

### Submit with a raw JSON string / IO stream

```python
import io

payload = '{"wordle": {"maxattempts": 2, "thinking_time": 1}}'
job = svc.request_job(io.StringIO(payload))
```

### Submit with a Pydantic model defined inline

```python
from pydantic import BaseModel, Field

class MyReq(BaseModel):
    duration_seconds: int = Field(60)
    throw_exception_at_end: bool = False

job = svc.request_job(MyReq())
```

---

## 6. Monitoring Jobs

> **Under the hood:** `job.refresh()` reads the job's latest `urn:ivcap:schema.job.2`
> aspect from the Datafabric. The job result (when available) is stored as a separate
> `urn:ivcap:schema.job-result.1` aspect linking the job entity to its result artifact
> or inline JSON content. This is why `job.result` may trigger a second network round-
> trip if it hasn't been fetched yet.

### Job status values (`JobStatus` enum)

```python
from ivcap_client import JobStatus

# Values: UNKNOWN, PENDING, SCHEDULED, EXECUTING, SUCCEEDED, FAILED, ERROR
```

### Poll until finished

```python
from time import sleep
from ivcap_client import JobStatus

while not job.finished:
    sleep(5)
    job.refresh()                    # update status from server

print(job.status())                  # JobStatus.SUCCEEDED / .FAILED / .ERROR
```

### Batch job monitoring with CSV logging

```python
import csv
from time import sleep, time

jobs = [svc.request_job(req) for _ in range(10)]

with open("results.csv", "w", newline="") as f:
    w = csv.writer(f)
    start = time()
    while True:
        sleep(10)
        elapsed = int(time() - start)
        done = sum(1 for j in jobs if j.finished)
        for j in jobs:
            j.refresh()
            w.writerow([elapsed, j.id, j.status().value])
        f.flush()
        print(f"Progress: {done}/{len(jobs)}")
        if done == len(jobs):
            break
```

### Access job result

```python
if job.status() == JobStatus.SUCCEEDED:
    result = job.result      # parsed response body (dict / object)
    print(result)
```

### Job properties

| Property/Method | Description |
|---|---|
| `job.id` | URN of the job |
| `job.status()` | Refresh and return current `JobStatus` |
| `job.finished` | `True` if SUCCEEDED, FAILED, or ERROR |
| `job.succeeded` | `True` only if SUCCEEDED |
| `job.result` | Result payload (fetched on demand) |
| `job.refresh()` | Pull latest state from the server |
| `job.requested_at` | When the job was submitted |
| `job.started_at` | When execution began |
| `job.finished_at` | When execution ended |

---

## 7. Artifacts — Upload & Download

Artifacts are binary or text blobs (images, CSV files, JSON, etc.) stored in IVCAP.
Each artifact has two parts: the **blob** (stored in GCS/S3 object storage, accessed
via the TUS protocol for writes and streaming HTTP for reads) and **Aspects** in the
Datafabric (describing its MIME type, size, provenance, and any domain metadata).

> **Artifact URNs as service inputs:** When a service parameter has type `ARTIFACT`,
> you pass the artifact's URN (`urn:ivcap:artifact:<uuid>`) as the parameter value.
> The service container can then download the artifact bytes via its local sidecar at
> `GET http://ivcap.local/1/artifacts/<uuid>/blob`.

### Upload a file

```python
artifact = ivcap.upload_artifact(
    name="my-image",
    file_path="/path/to/image.jpg",
    policy="urn:ivcap:policy:ivcap.open.artifact",  # optional, makes it public
)
print(artifact)
# <Artifact id=urn:ivcap:artifact:<uuid>, status=ready>
```

### Upload from an in-memory stream

```python
import io

data = b"col1,col2\n1,2\n3,4\n"
artifact = ivcap.upload_artifact(
    name="my-data.csv",
    io_stream=io.BytesIO(data),
    content_type="text/csv",
    content_size=len(data),
)
```

### Upload parameters

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Human-readable name for the artifact |
| `file_path` | `str` | Local path to upload |
| `io_stream` | `IO` | In-memory stream (requires `content_type`) |
| `content_type` | `str` | MIME type (auto-detected from `file_path` extension if omitted) |
| `content_size` | `int` | Size in bytes (-1 = unknown) |
| `collection` | `URN` | Add to a named collection (`urn:ivcap:collection:...`) |
| `policy` | `URN` | Access policy (`urn:ivcap:policy:...`) |
| `chunk_size` | `int` | TUS upload chunk size (default: max) |
| `retries` | `int` | Number of retry attempts on upload failure |
| `retry_delay` | `int` | Seconds between retries |
| `force_upload` | `bool` | Re-upload even if file was previously uploaded |

> **Deduplication:** The SDK automatically tracks uploaded files using a hidden
> `.ivcap-<filename>.txt` sidecar. If you call `upload_artifact` again for the same
> unchanged file, it will return the existing artifact without re-uploading.
> Override with `force_upload=True`.

### Check if a file was already uploaded

```python
artifact = ivcap.artifact_for_file("/path/to/file.jpg")
if artifact:
    print(f"Already uploaded as {artifact.id}")
```

### Get an artifact by URN

```python
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
print(artifact.name, artifact.size, artifact.mime_type)
```

### Download artifact content

Three methods are available, from most convenient to most low-level:

```python
# ── Recommended: download to a local file ────────────────────────────────────

# Temporary file (auto-deleted when the 'with' block exits)
with artifact.as_local_file() as path:
    print(f"Downloaded to {path}")
    data = path.read_bytes()
# temp file deleted here

# Explicit path (file is kept)
path = artifact.as_local_file("/tmp/output.jpg")
print(f"Saved to {path}")

# ── Load entirely into memory (suitable for small files) ─────────────────────
with artifact.open() as f:
    data = f.read()           # bytes

# ── Stream in chunks (advanced: progress, piping, incremental processing) ────
total = 0
with open("/tmp/output.jpg", "wb") as f:
    for chunk in artifact.as_stream():
        f.write(chunk)
        total += len(chunk)
print(f"Downloaded {total} bytes")
```

> **When running in local mode** (`LocalFileArtifact`), `as_local_file()`
> returns a `SafePath` to the pre-existing local file.  The file is
> **never deleted** on context exit.

### List artifacts

```python
for artifact in ivcap.list_artifacts(limit=20):
    print(artifact.id, artifact.name, artifact.mime_type)
    for meta in artifact.metadata:
        print(f"  schema: {meta.schema}")
```

### Artifact provenance in the Datafabric

Every upload and every artifact produced by a job is recorded as a set of Aspects:

- `urn:ivcap:schema.artifact.1` — MIME type, size, storage location
- `urn:ivcap:schema.artifact-produced-by-order` — link: artifact → job that created it
- `urn:ivcap:schema.artifact-used-by-order` — link: artifact → jobs that consumed it

These provenance aspects are written automatically by the platform. You can query them
with `ivcap.list_aspects(entity=artifact.id)` to reconstruct full data lineage.

### Local-file artifacts

When a job runs inside IVCAP the platform provides local file paths as artifact URNs:

```python
artifact = ivcap.get_artifact("file:///data/input.csv")
# Returns a LocalFileArtifact — open()/as_local_file() work without network calls
```

---

## 8. Aspects — Metadata on Any Entity

Aspects are typed JSON documents attached to any IVCAP entity (artifact, service,
job, etc.). They form the **Datafabric** — the universal, append-only,
provenance-preserving knowledge graph of the entire IVCAP platform.

As an agent you interact with aspects in two distinct roles:

1. **Reading platform state** — job status, service descriptions, artifact metadata, and
   all provenance records are all aspects. The `list_aspects()` API lets you query any
   of them.
2. **Attaching your own domain knowledge** — you can annotate any entity (artifact, job,
   or any custom entity URN) with any JSON payload under any schema you choose.
   These annotations are first-class platform objects: they are access-controlled,
   versioned, time-stamped, and queryable.

> **Immutability:** `add_aspect` creates a **new** assertion; if a prior aspect with the
> same `(entity, schema)` pair exists, both remain valid concurrently. Use
> `update_aspect` when you want to **replace** a prior assertion — it retracts the old
> one first by setting its `validTo = now`. Use `retract()` to close an aspect without
> replacing it.

### Add an aspect to an entity

```python
aspect = ivcap.add_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:image-annotation.1",
        "label": "cat",
        "confidence": 0.97,
    },
)
print(aspect)
```

### Update (replace) an existing aspect

`update_aspect` retracts any previous aspect with the same `(entity, schema)` pair
before creating the new one:

```python
aspect = ivcap.update_aspect(
    entity="urn:ivcap:artifact:<uuid>",
    aspect={
        "$schema": "urn:my-project:schema:image-annotation.1",
        "label": "dog",
        "confidence": 0.88,
    },
)
```

### Add metadata directly to an artifact

```python
artifact = ivcap.get_artifact("urn:ivcap:artifact:<uuid>")
artifact.add_metadata({
    "$schema": "urn:my:schema:tag.1",
    "tags": ["marine", "coral"],
})
```

### List / search aspects

```python
# All aspects with a given schema
for aspect in ivcap.list_aspects(
    schema="urn:common:schema:in_collection.1",
    limit=20,
    include_content=True,
):
    print(aspect.entity, aspect.schema)
    print(aspect.aspect)           # the JSON content dict

# Aspects for a specific entity
for aspect in ivcap.list_aspects(entity="urn:ivcap:artifact:<uuid>"):
    print(aspect.schema)
```

**`list_aspects()` parameters:**

| Parameter | Description |
|---|---|
| `entity` | Filter by entity URN |
| `schema` | Filter by schema prefix (supports `%` wildcard) |
| `content_path` | JSONPath filter applied to aspect content |
| `at_time` | Historical snapshot time |
| `limit` | Max items (default 10) |
| `filter` | OData-style filter expression |
| `order_by` | Sort field (default `valid_from`) |
| `order_direction` | `"ASC"` or `"DESC"` (default `"DESC"`) |
| `include_content` | Include aspect JSON content in listing (default `True`) |

### Query aspects at a point in time

Because the Datafabric is append-only, you can reconstruct the exact state of any entity
at any past moment:

```python
from datetime import datetime, timezone

past = datetime(2025, 1, 1, tzinfo=timezone.utc)
for aspect in ivcap.list_aspects(
    entity="urn:ivcap:artifact:<uuid>",
    at_time=past,
    include_content=True,
):
    print(f"Valid from {aspect.valid_from}: {aspect.schema}")
    print(aspect.aspect)
```

### Retract an aspect

```python
aspects = list(ivcap.list_aspects(entity="urn:ivcap:artifact:<uuid>", schema="urn:my:schema:tag.1"))
if aspects:
    aspects[0].retract()
```

---

## 9. Secrets

```python
for secret in ivcap.list_secrets(limit=50):
    print(secret)
```

---

## 10. Agents

Agents are services that follow an agent pattern (they wrap a `Service` internally).

```python
agent = ivcap.get_agent("urn:ivcap:service:<uuid>")

# Get the Pydantic request model
Model = agent.request_model

# Execute the agent and wait for completion (blocks until done)
job = agent.exec_agent(Model(some_param="value"))
print(job.result)
```

`exec_agent()` submits the job and polls until `job.finished`, then returns the `Job`.

---

## 11. Search (Datalog)

IVCAP supports a Datalog/Mangle query language over its knowledge graph. The search
service traverses the *emergent graph* formed by URN references embedded in aspect
content — for example, the link from a job aspect to the service URN, or from a
job-result aspect to an artifact URN. This allows queries such as "find all artifacts
produced by jobs that used this particular service version".

```python
# ivcap.search() expects a str query, not bytes
query = """
:- ivcap_artifact(Id, Name, MimeType),
   MimeType = "image/jpeg".
"""

results = ivcap.search(query)
for r in results.items:
    print(r)
```

---

## 12. Error Handling

Import exceptions from `ivcap_client.exception`:

```python
from ivcap_client.exception import (
    IvcapError,          # base class for all IVCAP exceptions
    IvcapApiError,       # HTTP error from the API (has .status_code, .operation)
    NotAuthorizedException,  # HTTP 401/403
    ResourceNotFound,    # service or artifact not found
    AmbiguousRequest,    # get_service_by_name matched more than one service
    MissingParameterValue,   # required parameter missing when creating an aspect
)
```

### Typical patterns

```python
from ivcap_client.exception import ResourceNotFound, AmbiguousRequest

try:
    service = ivcap.get_service_by_name("my-service")
except ResourceNotFound as e:
    print(f"Service not found: {e.resource}")
except AmbiguousRequest as e:
    print(f"Ambiguous: {e}")
```

```python
from ivcap_client.exception import IvcapApiError

try:
    artifact = ivcap.upload_artifact(file_path="/tmp/data.csv")
except IvcapApiError as e:
    print(f"Upload failed [{e.status_code}]: {e}")
```

### Job failure detection

```python
from ivcap_client import JobStatus

job = svc.request_job(req)
while not job.finished:
    job.refresh()

if job.status() == JobStatus.SUCCEEDED:
    print("Done:", job.result)
elif job.status() == JobStatus.FAILED:
    print("Job reported failure")
elif job.status() == JobStatus.ERROR:
    print("Job encountered an internal error")
```

---

## 13. Async Usage

All major operations have `_async` variants that are compatible with `asyncio`.

### Async job submission and waiting

```python
import asyncio
from ivcap_client.ivcap import IVCAP

async def run():
    ivcap = IVCAP()
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")

    # Fetch request model asynchronously
    Model = await svc.request_model_async()
    req = Model(duration_seconds=2)

    # Submit and wait until the job finishes
    job = await svc.request_job_async(req)
    result = await job.result_async()
    print(result)

asyncio.run(run())
```

### Async polling loop

```python
async def run():
    job = await svc.request_job_async(req, max_wait_time=None)
    while not await job.finished_async():
        await asyncio.sleep(5)
    status = await job.status_async(refresh=False)
    print(status)
```

### Parallel jobs (async)

```python
async def run():
    svc = ivcap.get_service("urn:ivcap:service:<uuid>")
    Model = await svc.request_model_async()
    req = Model(**payload)

    jobs = [svc.request_job(req, timeout=0) for _ in range(5)]

    running = set(jobs)
    while running:
        job = running.pop()
        status = job.status(refresh=True)
        if not job.finished:
            running.add(job)
        await asyncio.sleep(5)
```

---

## 14. Environment Variable Reference

| Variable | Description | Used by |
|---|---|---|
| `IVCAP_URL` | External URL of IVCAP deployment — triggers platform mode | `IVCAP()` |
| `IVCAP_BASE_URL` | Internal URL injected by the platform inside a job container — no JWT needed | `IVCAP()` |
| `IVCAP_JWT` | JWT bearer token for authentication (external access only) | `IVCAP()` |
| `IVCAP_ACCOUNT_ID` | Account URN for artifact/aspect ownership | Application code |
| `IVCAP_LOCAL_DIR` | Root directory for local artifact storage in **local mode** (default: `ivcap-artifacts`) | `IVCAP()`, `IVCAP.local()`, `LocalIVCAP` |

**Mode selection summary:**

| Environment | `IVCAP()` returns |
|---|---|
| `IVCAP_URL` set + `IVCAP_JWT` set | Platform `IVCAP` (external) |
| `IVCAP_BASE_URL` set (inside container) | Platform `IVCAP` (no token needed) |
| Neither URL set, no explicit token | `LocalIVCAP` (filesystem, no network) |

---

## Quick-Start Cheatsheet

```python
from dotenv import load_dotenv
from ivcap_client.ivcap import IVCAP
from ivcap_client import JobStatus

load_dotenv('.dbg-env')
ivcap = IVCAP()

# --- Discover ---
svc = ivcap.get_service_by_name("my-service")
print(svc, svc.mandatory_parameters)

# --- Run ---
Model = svc.request_model
job = svc.request_job(Model(param="value"))

# --- Poll ---
while not job.finished:
    job.refresh()
if job.status() == JobStatus.SUCCEEDED:
    print(job.result)

# --- Artifacts ---
art = ivcap.upload_artifact(file_path="/tmp/data.csv")
ivcap.get_artifact(art.id)
with art.as_local_file() as p:
    data = p.read_bytes()

# --- Aspects ---
ivcap.add_aspect(art.id, {"$schema": "urn:my:schema:tag.1", "tag": "test"})
for a in ivcap.list_aspects(entity=art.id):
    print(a.aspect)
```
