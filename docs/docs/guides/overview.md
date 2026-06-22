# Guides Overview

These guides provide in-depth coverage of the IVCAP Client SDK's features and patterns.

## Getting Started

If you're new to the SDK, start here:

1. **[Installation](../getting-started/installation.md)** — Set up the SDK
2. **[Quick Start](../getting-started/quick-start.md)** — 5-minute introduction
3. **[Authentication](../getting-started/authentication.md)** — Configure credentials

## Core Workflows

### [Discovering Services](services.md)

Find and inspect the analytic services available on your IVCAP deployment:
- Listing all services with `list_services()`
- Finding a service by name with `get_service_by_name()`
- Inspecting parameters and request models
- Filtering and ordering results

**Read this if:** You want to explore what services are available and understand their inputs.

### [Running Jobs](jobs.md)

Submit and monitor service executions:
- Synchronous and asynchronous job submission
- Timeout strategies (`timeout=0` vs. blocking)
- Polling with `job.refresh()` and `job.finished`
- Accessing results via `job.result`
- Batch job monitoring

**Read this if:** You want to submit work to IVCAP services and retrieve results.

### [Working with Artifacts](artifacts.md)

Upload data, download results, and manage binary blobs:
- Uploading files and in-memory streams
- Automatic deduplication via sidecar files
- Streaming and downloading artifacts
- Using artifact URNs as service inputs
- Working with collections

**Read this if:** Your workflow involves data files (images, CSV, NetCDF, models, etc.).

### [The Datafabric & Aspects](aspects.md)

Read and write typed metadata on any platform entity:
- Understanding the Datafabric (append-only, versioned assertions)
- Adding and updating aspects
- Listing and querying aspects by schema or entity
- Historical snapshots with `at_time`
- Retracting aspects

**Read this if:** You need to attach, query, or update metadata on jobs, artifacts, or custom entities.

## Advanced Topics

### [Async Usage](async-usage.md)

Use the SDK with Python's `asyncio`:
- `_async` variants of all major operations
- Async job submission and polling
- Running many jobs in parallel with `asyncio.gather()`

**Read this if:** You're building async applications or want to run many jobs concurrently.

### [Error Handling](error-handling.md)

Build robust code with proper exception handling:
- All exception types and when they're raised
- Handling `ResourceNotFound`, `AmbiguousRequest`, `IvcapApiError`
- Job failure vs. platform error (`FAILED` vs. `ERROR`)
- Retry patterns

**Read this if:** You need production-grade error handling.

### [Local Mode & Mode Selection](local-mode.md)

Understand the three ways to obtain an `IVCAP` instance and how to test service logic
locally without a platform:
- The three operating modes (external platform, in-container, local)
- ENV-variable-driven auto-detection — `IVCAP()` picks the right mode automatically
- Using `LocalIVCAP` to run and test services before deployment
- Forcing local mode in unit tests with `IVCAP.local()`
- What `LocalIVCAP` supports vs. platform-only operations

**Read this if:** You are developing or testing an IVCAP service locally, or want to
understand how the same `IVCAP()` call works in every environment.

### [Agent Integration](agents.md)

Use IVCAP services inside AI agents:
- The `Agent` wrapper class
- `exec_agent()` for blocking agent execution
- Async agent patterns

**Read this if:** You're building AI agents that need to invoke IVCAP capabilities.

### [Search (Datalog)](search.md)

Query the IVCAP knowledge graph with Datalog/Mangle:
- Writing Datalog queries
- Using `ivcap.search()` to traverse the graph
- Useful query patterns

**Read this if:** You need to query provenance or discover entities through graph traversal.

## Learning Path

```
Installation
    ↓
Quick Start
    ↓
Discovering Services
    ↓
Running Jobs
    ├→ Working with Artifacts (if your workflow uses data files)
    ├→ The Datafabric & Aspects (if you need metadata)
    ├→ Local Mode & Mode Selection (if you are building/testing a service)
    └→ Async Usage (if you need parallel execution)
    ↓
Error Handling
    ↓
Agent Integration (optional, for AI agents)
```

## See Also

- **[API Reference](../api/overview.md)** — Complete class and method documentation
- **[Examples](../examples/overview.md)** — Ready-to-run scripts
- **[Reference](../reference/environment-variables.md)** — Configuration reference
