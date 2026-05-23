# Glossary

Key terms and concepts used in the IVCAP Client SDK.

## Artifact

A binary or structured data blob stored in the IVCAP platform — images, CSV files,
NetCDF datasets, model checkpoints, etc. An artifact has two parts: the raw blob
(stored in GCS/S3-compatible object storage) and metadata aspects in the Datafabric.

## Aspect

A typed, time-bounded assertion attached to any entity URN. Aspects are the building
blocks of the Datafabric. They are immutable once created — "updates" create a new
aspect and retract the old one, preserving the full history.

## Datafabric

IVCAP's single source of truth for all platform state. An append-only, aspect-oriented,
provenance-preserving information store. Every job status update, service description,
artifact metadata record, and provenance link is an aspect in the Datafabric.

## Dispatcher

The platform component that launches service containers. IVCAP has four dispatchers:
Lambda (long-running K8s Deployment), Batch (fresh K8s Job per invocation), Nextflow
(Nextflow pipeline), and Argo (Argo Workflow).

## Job

One invocation of a service. A job tracks the full lifecycle from `pending` through
`executing` to `succeeded` or `failed`/`error`. The job record is an aspect in the
Datafabric under schema `urn:ivcap:schema.job.2`.

## JobContext (service-side)

The context object passed to a service's job-processing function when running inside
an IVCAP service container. Not relevant to client-side SDK usage. See the
[ivcap-service-sdk](https://pypi.org/project/ivcap_service/).

## JWT (JSON Web Token)

The access credential used to authenticate with the IVCAP API. Obtained via the
[ivcap-cli](https://github.com/reinventingscience/ivcap-cli) with
`ivcap context get access-token`.

## Order

The legacy name for a job invocation. Orders and jobs share the same underlying
Datafabric representation. The Orders API is still fully supported.

## Policy

An access control descriptor (`urn:ivcap:policy:<name>`) that governs who can read
or retract an artifact or aspect. Common policies include
`urn:ivcap:policy:ivcap.open.artifact` for publicly readable artifacts.

## Provenance

The chain of evidence linking artifacts to the jobs that produced and consumed them,
and jobs to the services that executed them. Provenance is recorded automatically as
aspects in the Datafabric.

## Request Model

A Pydantic `BaseModel` class dynamically constructed from a service's
`urn:sd-core:schema.ai-tool.1` aspect. Use `service.request_model` to access it.

## Schema

A URN identifying the shape and meaning of an aspect's JSON content. Well-known
platform schemas use `urn:ivcap:schema.*`. You can use any URN for your own schemas.

## Service

A registered, executable analytic capability on the IVCAP platform. Services are
Docker images with a defined input/output schema, published by providers and
discoverable by any authorised client.

## Service Sidecar

A platform-managed component running alongside each service container in Kubernetes.
Handles authentication, artifact I/O, and result reporting on behalf of the service.
Transparent to client-side SDK users.

## TUS Protocol

The resumable upload protocol used by IVCAP for artifact uploads. The SDK handles TUS
transparently — you just call `ivcap.upload_artifact()`.

## URN (Uniform Resource Name)

The globally unique identifier for every IVCAP entity. Format:
`urn:ivcap:<type>:<uuid>`.

| Entity type | URN pattern |
|---|---|
| Service | `urn:ivcap:service:<uuid>` |
| Job | `urn:ivcap:job:<uuid>` |
| Order | `urn:ivcap:order:<uuid>` |
| Artifact | `urn:ivcap:artifact:<uuid>` |
| Aspect | `urn:ivcap:aspect:<uuid>` |
| Account | `urn:ivcap:account:<uuid>` |
| Policy | `urn:ivcap:policy:<name>` |

## See Also

- [API Reference](../api/overview.md)
- [Getting Started](../getting-started/quick-start.md)
