"""Tests for resumable artifact downloads (Range + ETag validation).

All tests use an in-process fake blob server (httpx.MockTransport), so there is
no network access. The fake mirrors the live IVCAP blob endpoint, which was
checked with curl: it answers ``Range`` with ``206`` and ``Content-Range``, sends
an unquoted ETag on every response, and ignores ``If-Range``. The ETag is not the
MD5 of the content, so the fake uses an opaque value too.
"""

import httpx
import pytest

from ivcap_client.artifact import Artifact
from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import IvcapError
from ivcap_client.ivcap import IVCAP

BASE_URL = "http://test"
BLOB_PATH = "/1/artifacts/urn:ivcap:artifact:abc/blob"
CONTENT = bytes(range(256)) * 400  # 102400 bytes
ETAG = "90dba55fd62050a8f0d2937c0c07f549"


class _TruncatedStream(httpx.SyncByteStream):
    """Yields the given bytes, then raises as if the peer closed the connection."""

    def __init__(self, body: bytes):
        self._body = body

    def __iter__(self):
        yield self._body
        raise httpx.RemoteProtocolError(
            "peer closed connection without sending complete message body"
        )


class FakeBlobServer:
    """Serves CONTENT like the live endpoint and can drop connections early.

    ``drop_after``: one entry per GET; each is the number of body bytes sent before
    the connection is cut. Once the list is exhausted, responses complete.
    """

    def __init__(
        self, content: bytes = CONTENT, etag: str | None = ETAG, drop_after=None
    ):
        self.content = content
        self.etag = etag
        self.drop_after = list(drop_after or [])
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        assert request.url.path == BLOB_PATH
        headers = {"ETag": self.etag} if self.etag else {}
        start = 0
        rng = request.headers.get("range")
        if rng:
            start = int(rng.removeprefix("bytes=").rstrip("-"))
            if start >= len(self.content):
                return httpx.Response(416, headers=headers)
            headers["Content-Range"] = (
                f"bytes {start}-{len(self.content) - 1}/{len(self.content)}"
            )
        status = 206 if rng else 200
        body = self.content[start:]
        if self.drop_after:
            limit = self.drop_after.pop(0)
            headers["Content-Length"] = str(len(body))
            return httpx.Response(
                status, stream=_TruncatedStream(body[:limit]), headers=headers
            )
        return httpx.Response(status, content=body, headers=headers)


def _make_artifact(
    server: FakeBlobServer, size: int | None = None, handler=None
) -> Artifact:
    transport = httpx.MockTransport(handler or server.handler)
    iv = IVCAP(url=BASE_URL, token="token")
    iv._client = AuthenticatedClient(
        base_url=BASE_URL, token="token", httpx_args={"transport": transport}
    )
    return Artifact(
        iv,
        id="urn:ivcap:artifact:abc",
        status=None,
        **{
            "mime-type": "application/octet-stream",
            "size": size if size is not None else len(server.content),
            "data-href": f"{BASE_URL}{BLOB_PATH}",
        },
    )


def test_resume_after_premature_close_yields_identical_bytes():
    # Drops land on chunk boundaries (8192), so each attempt delivers whole chunks.
    server = FakeBlobServer(drop_after=[32_768, 49_152])
    art = _make_artifact(server)

    data = b"".join(art.as_stream(chunk_size=8192, retry_delay=0))

    assert data == CONTENT
    assert len(server.requests) == 3
    assert "range" not in server.requests[0].headers
    assert server.requests[1].headers["range"] == "bytes=32768-"
    assert server.requests[2].headers["range"] == "bytes=81920-"


def test_resume_is_not_sent_with_if_range():
    # The live endpoint answers If-Range with 200 and the full body, so it is not sent.
    server = FakeBlobServer(drop_after=[8192])
    art = _make_artifact(server)

    b"".join(art.as_stream(chunk_size=4096, retry_delay=0))

    assert "if-range" not in server.requests[1].headers


def test_resume_accepts_matching_etag_on_partial_response():
    server = FakeBlobServer(drop_after=[8192])
    art = _make_artifact(server)

    assert b"".join(art.as_stream(chunk_size=4096, retry_delay=0)) == CONTENT


def test_resume_rejects_changed_etag():
    first = FakeBlobServer(drop_after=[8192])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("range"):
            # Same content range, but the blob was replaced in the meantime.
            return httpx.Response(
                206,
                content=CONTENT[8192:],
                headers={
                    "ETag": "0000000000000000000000000000dead",
                    "Content-Range": f"bytes 8192-{len(CONTENT) - 1}/{len(CONTENT)}",
                },
            )
        return first.handler(request)

    art = _make_artifact(FakeBlobServer(), handler=handler)
    with pytest.raises(IvcapError, match="ETag changed"):
        b"".join(art.as_stream(chunk_size=4096, retry_delay=0))


def test_missing_etag_still_resumes_without_validation():
    server = FakeBlobServer(etag=None, drop_after=[8192])
    art = _make_artifact(server)

    assert b"".join(art.as_stream(chunk_size=4096, retry_delay=0)) == CONTENT


def test_changed_blob_is_rejected_when_server_ignores_range():
    # The server ignores Range and answers 200 with a whole new body.
    first = FakeBlobServer(drop_after=[8192])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("range"):
            return httpx.Response(
                200, content=b"x" * len(CONTENT), headers={"ETag": "other"}
            )
        return first.handler(request)

    art = _make_artifact(FakeBlobServer(), handler=handler)
    with pytest.raises(IvcapError, match="did not honour Range"):
        b"".join(art.as_stream(chunk_size=4096, retry_delay=0))


def test_bad_content_range_start_is_rejected():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.headers.get("range"):
            return httpx.Response(
                206,
                content=CONTENT[5:],
                headers={
                    "ETag": ETAG,
                    "Content-Range": f"bytes 5-{len(CONTENT) - 1}/{len(CONTENT)}",
                },
            )
        return httpx.Response(
            200, stream=_TruncatedStream(CONTENT[:8192]), headers={"ETag": ETAG}
        )

    art = _make_artifact(FakeBlobServer(), handler=handler)
    with pytest.raises(IvcapError, match="Content-Range"):
        b"".join(art.as_stream(chunk_size=4096, retry_delay=0))


def test_retries_exhausted_raises_original_error():
    # No progress per attempt (drop before the first 64-byte chunk), so retries accumulate.
    server = FakeBlobServer(drop_after=[10, 10, 10])
    art = _make_artifact(server)

    with pytest.raises(httpx.RemoteProtocolError):
        b"".join(art.as_stream(chunk_size=64, max_retries=2, retry_delay=0))
    assert len(server.requests) == 3


def test_failure_counter_resets_after_progress():
    # Five drops, each after progress; max_retries=1 only works if the counter resets.
    server = FakeBlobServer(drop_after=[500, 500, 500, 500, 500])
    art = _make_artifact(server)

    assert (
        b"".join(art.as_stream(chunk_size=256, max_retries=1, retry_delay=0)) == CONTENT
    )


def test_body_longer_than_declared_size_raises():
    server = FakeBlobServer()
    art = _make_artifact(server, size=len(CONTENT) - 10)
    with pytest.raises(IvcapError, match="expected"):
        b"".join(art.as_stream(retry_delay=0))


def test_as_local_file_resumes_and_writes_full_content(tmp_path):
    # Auto chunk size for 102400 bytes is 10240; drop after 3 full chunks.
    server = FakeBlobServer(drop_after=[30_720])
    art = _make_artifact(server)

    path = art.as_local_file(tmp_path / "out.bin", retry_delay=0)

    assert path.read_bytes() == CONTENT
    assert server.requests[1].headers["range"] == "bytes=30720-"


def test_downloaded_path_opens_read_only_binary_by_default(tmp_path):
    server = FakeBlobServer()
    art = _make_artifact(server)

    path = art.as_local_file(tmp_path / "ro.bin")

    with path.open() as f:
        assert f.read(4) == CONTENT[:4]
    with path.open("rb") as f:
        assert f.read(4) == CONTENT[:4]


def test_downloaded_path_refuses_write_modes(tmp_path):
    server = FakeBlobServer()
    art = _make_artifact(server)
    path = art.as_local_file(tmp_path / "ro.bin")

    for mode in ("wb", "ab", "r+b", "xb"):
        with pytest.raises(ValueError, match="read-only"):
            path.open(mode)
    assert path.read_bytes() == CONTENT


def test_downloaded_path_allows_text_read_on_request(tmp_path):
    text = "héllo, wörld\n".encode() * 50
    server = FakeBlobServer(content=text, etag=None)
    art = _make_artifact(server)
    path = art.as_local_file(tmp_path / "text.txt")

    with path.open("r", encoding="utf-8") as f:
        assert f.readline() == "héllo, wörld\n"
    with path.open("rt", encoding="utf-8") as f:
        assert f.read() == text.decode("utf-8")
    assert path.read_text(encoding="utf-8") == text.decode("utf-8")
    assert path.open("rb").read() == text
