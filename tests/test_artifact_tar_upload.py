"""Tests for streaming tar-archive creation + chunked TUS upload.

All tests use an in-process fake TUS server (httpx.MockTransport) — no real
network access. Covers: TarMember validation, end-to-end upload (files +
in-memory bytes), chunking behaviour, retry/resume-after-failure, and error
propagation from the archive-building thread.
"""

import io
import tarfile

import httpx
import pytest

from ivcap_client.artifact import TarMember, upload_tar_artifact
from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import IvcapApiError
from ivcap_client.ivcap import IVCAP

# ---------------------------------------------------------------------------
# TarMember validation
# ---------------------------------------------------------------------------


def test_tar_member_requires_exactly_one_source():
    with pytest.raises(ValueError):
        TarMember(arcname="x")  # neither file_path nor data
    with pytest.raises(ValueError):
        TarMember(arcname="x", file_path="/tmp/a", data=b"y")  # both


def test_tar_member_from_file_default_arcname(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("hi")
    m = TarMember.from_file(str(f))
    assert m.arcname == "hello.txt"
    assert m.file_path == str(f)


def test_tar_member_from_bytes():
    m = TarMember.from_bytes(b"content", arcname="data.bin")
    assert m.data == b"content"
    assert m.arcname == "data.bin"


# ---------------------------------------------------------------------------
# Fake in-process TUS server
# ---------------------------------------------------------------------------


class _FakeTusServer:
    """A minimal in-memory TUS server used to drive the real upload code
    path through httpx.MockTransport, with no actual network I/O."""

    def __init__(self, fail_first_n_patches: int = 0):
        self.storage = bytearray()
        self.upload_path = "/1/artifacts/urn:ivcap:artifact:abc/blob"
        self.create_requests: list[httpx.Request] = []
        self.patch_requests: list[httpx.Request] = []
        self.head_requests: list[httpx.Request] = []
        self._fail_first_n_patches = fail_first_n_patches
        self._patch_call_count = 0

    def handler(self, request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            self.create_requests.append(request)
            assert request.headers.get("upload-defer-length") == "1"
            return httpx.Response(
                201, headers={"Location": self.upload_path, "Tus-Resumable": "1.0.0"}
            )
        if request.method == "HEAD":
            self.head_requests.append(request)
            return httpx.Response(
                200,
                headers={
                    "Upload-Offset": str(len(self.storage)),
                    "Tus-Resumable": "1.0.0",
                },
            )
        if request.method == "PATCH":
            self.patch_requests.append(request)
            self._patch_call_count += 1
            if self._patch_call_count <= self._fail_first_n_patches:
                return httpx.Response(500, text="simulated failure")
            offset = int(request.headers["upload-offset"])
            assert offset == len(self.storage)
            self.storage.extend(request.content)
            return httpx.Response(
                204,
                headers={
                    "Upload-Offset": str(len(self.storage)),
                    "Tus-Resumable": "1.0.0",
                },
            )
        raise AssertionError(f"unexpected method {request.method}")


def _make_ivcap_with_fake_tus(server: _FakeTusServer) -> IVCAP:
    base_url = "http://test"

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/1/artifacts" and request.method == "POST":
            return httpx.Response(
                201,
                json={
                    "id": "urn:ivcap:artifact:abc",
                    "status": "pending",
                    "links": [],
                    "data-href": f"{base_url}{server.upload_path}",
                    "mime-type": "application/gzip",
                },
            )
        if request.method == "GET" and "/1/artifacts/" in request.url.path:
            # Artifact.refresh()'s status GET, issued after the upload
            # completes (a.status forces a refresh).
            return httpx.Response(
                200,
                json={
                    "id": "urn:ivcap:artifact:abc",
                    "status": "ready",
                    "links": [],
                    "data-href": f"{base_url}{server.upload_path}",
                    "mime-type": "application/gzip",
                    "size": len(server.storage),
                },
            )
        return server.handler(request)

    transport = httpx.MockTransport(handler)
    iv = IVCAP(url=base_url, token="token")
    iv._client = AuthenticatedClient(
        base_url=base_url, token="token", httpx_args={"transport": transport}
    )
    return iv


def _extract_tar_gz(data: bytes) -> dict[str, bytes]:
    out = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar:
            if member.isfile():
                f = tar.extractfile(member)
                out[member.name] = f.read()
    return out


# ---------------------------------------------------------------------------
# End-to-end upload
# ---------------------------------------------------------------------------


def test_upload_tar_artifact_files_and_bytes(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_bytes(b"aaaa" * 100)
    f2 = tmp_path / "b.txt"
    f2.write_bytes(b"bbbb" * 100)

    members = [
        TarMember.from_file(str(f1)),
        TarMember.from_file(str(f2), arcname="renamed-b.txt"),
        TarMember.from_bytes(b"in-memory content", arcname="c.txt"),
    ]

    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)

    artifact = upload_tar_artifact(iv, members, name="bundle.tar.gz")

    assert artifact.id == "urn:ivcap:artifact:abc"
    extracted = _extract_tar_gz(bytes(server.storage))
    assert extracted["a.txt"] == b"aaaa" * 100
    assert extracted["renamed-b.txt"] == b"bbbb" * 100
    assert extracted["c.txt"] == b"in-memory content"

    # Final PATCH must carry Upload-Length to complete the deferred upload.
    final_patch = server.patch_requests[-1]
    assert "upload-length" in final_patch.headers
    assert int(final_patch.headers["upload-length"]) == len(server.storage)


def test_upload_tar_artifact_via_ivcap_method(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_bytes(b"hello world")
    members = [TarMember.from_file(str(f1))]

    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)

    artifact = iv.upload_tar_artifact(members, name="bundle.tar.gz")

    assert artifact.id == "urn:ivcap:artifact:abc"
    extracted = _extract_tar_gz(bytes(server.storage))
    assert extracted["a.txt"] == b"hello world"


def test_upload_tar_artifact_uses_small_chunk_size_multiple_patches(tmp_path):
    import random

    rng = random.Random(42)
    content = bytes(rng.getrandbits(8) for _ in range(50_000))  # incompressible
    f1 = tmp_path / "big.bin"
    f1.write_bytes(content)
    members = [TarMember.from_file(str(f1))]

    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)

    artifact = upload_tar_artifact(
        iv, members, name="bundle.tar.gz", chunk_size=1024, queue_maxsize=2
    )

    assert artifact.id == "urn:ivcap:artifact:abc"
    # With a tiny chunk size, the upload must have required several PATCHes.
    assert len(server.patch_requests) > 1
    extracted = _extract_tar_gz(bytes(server.storage))
    assert extracted["big.bin"] == content


def test_upload_tar_artifact_empty_members_list():
    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)

    artifact = upload_tar_artifact(iv, [], name="empty.tar.gz")

    assert artifact.id == "urn:ivcap:artifact:abc"
    extracted = _extract_tar_gz(bytes(server.storage))
    assert extracted == {}


# ---------------------------------------------------------------------------
# Retry / resume behaviour
# ---------------------------------------------------------------------------


def test_upload_tar_artifact_retries_after_transient_failure(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_bytes(b"retry-me" * 1000)
    members = [TarMember.from_file(str(f1))]

    # Fail the very first PATCH once, then succeed on retry.
    server = _FakeTusServer(fail_first_n_patches=1)
    iv = _make_ivcap_with_fake_tus(server)

    artifact = upload_tar_artifact(
        iv,
        members,
        name="bundle.tar.gz",
        chunk_size=1024,
        retries=3,
        retry_delay=0.01,
    )

    assert artifact.id == "urn:ivcap:artifact:abc"
    assert len(server.head_requests) >= 1  # re-synced offset after failure
    extracted = _extract_tar_gz(bytes(server.storage))
    assert extracted["a.txt"] == b"retry-me" * 1000


def test_upload_tar_artifact_raises_after_exhausting_retries(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_bytes(b"x" * 100)
    members = [TarMember.from_file(str(f1))]

    # Always fail every PATCH.
    server = _FakeTusServer(fail_first_n_patches=10_000)
    iv = _make_ivcap_with_fake_tus(server)

    with pytest.raises(IvcapApiError):
        upload_tar_artifact(
            iv, members, name="bundle.tar.gz", retries=2, retry_delay=0.01
        )


# ---------------------------------------------------------------------------
# Error propagation from the archive-building thread
# ---------------------------------------------------------------------------


def test_upload_tar_artifact_propagates_missing_file_error():
    members = [TarMember.from_file("/no/such/file/exists.txt")]

    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)

    with pytest.raises((FileNotFoundError, OSError)):
        upload_tar_artifact(iv, members, name="bundle.tar.gz")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_upload_tar_artifact_rejects_bad_collection():
    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)
    with pytest.raises(ValueError, match="URN"):
        upload_tar_artifact(iv, [], collection="not-a-urn")


def test_upload_tar_artifact_rejects_bad_policy():
    server = _FakeTusServer()
    iv = _make_ivcap_with_fake_tus(server)
    with pytest.raises(ValueError, match="policy"):
        upload_tar_artifact(iv, [], policy="urn:not:a:policy")
