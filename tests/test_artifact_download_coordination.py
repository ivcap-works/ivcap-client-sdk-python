"""Tests for crash-safe, thread-coordinated ``as_local_file(path, ...)`` downloads.

Covers the ``.part`` file + atomic rename, the ``.<name>.ivcap`` completion
marker, ``reuse_if_exists`` / ``verify_if_exists`` and sharing one download between
threads.  All offline: an in-process fake blob server (httpx.MockTransport).
"""

import json
import logging
import threading
import time

import httpx
import pytest

import ivcap_client.artifact as artifact_module
from ivcap_client.artifact import Artifact, DataUrlArtifact
from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.ivcap import IVCAP

BASE_URL = "http://test"
BLOB_PATH = "/1/artifacts/urn:ivcap:artifact:abc/blob"
URN = "urn:ivcap:artifact:abc"
CONTENT = bytes(range(256)) * 400  # 102400 bytes
ETAG = "90dba55fd62050a8f0d2937c0c07f549"
WAIT = 10  # seconds; generous upper bound for synchronisation in tests


class _TruncatedStream(httpx.SyncByteStream):
    def __init__(self, body: bytes):
        self._body = body

    def __iter__(self):
        yield self._body
        raise httpx.RemoteProtocolError("peer closed connection")


class _GatedStream(httpx.SyncByteStream):
    """Sends the first part of the body, then blocks until the gate opens."""

    def __init__(self, body: bytes, first_len: int, gate, started):
        self._body, self._first, self._gate, self._started = (
            body,
            first_len,
            gate,
            started,
        )

    def __iter__(self):
        yield self._body[: self._first]
        self._started.set()
        assert self._gate.wait(WAIT), "gate never opened"
        yield self._body[self._first :]


class FakeServer:
    def __init__(
        self,
        content: bytes = CONTENT,
        *,
        etag: str | None = ETAG,
        gate: threading.Event | None = None,
        drop_after: int | None = None,
        first_status: int | None = None,
    ):
        self.content = content
        self.etag = etag
        self.gate = gate
        self.drop_after = drop_after
        self.first_status = first_status
        self.started = threading.Event()  # set once a gated body is mid-flight
        self.first_started = threading.Event()  # set when request #1 arrived
        self.first_hold = threading.Event()  # request #1 waits for this (first_status)
        self.requests: list[httpx.Request] = []
        self._lock = threading.Lock()

    def handler(self, request: httpx.Request) -> httpx.Response:
        with self._lock:
            self.requests.append(request)
            n = len(self.requests)
        if n == 1 and self.first_status is not None:
            self.first_started.set()
            assert self.first_hold.wait(WAIT)
            return httpx.Response(self.first_status)
        headers = {"ETag": self.etag} if self.etag else {}
        if self.drop_after is not None:
            headers["Content-Length"] = str(len(self.content))
            return httpx.Response(
                200,
                stream=_TruncatedStream(self.content[: self.drop_after]),
                headers=headers,
            )
        if self.gate is not None:
            return httpx.Response(
                200,
                stream=_GatedStream(self.content, 2048, self.gate, self.started),
                headers=headers,
            )
        return httpx.Response(200, content=self.content, headers=headers)


def _make_artifact(
    server: FakeServer, *, etag: str | None = None, size: int | None = -1
) -> Artifact:
    iv = IVCAP(url=BASE_URL, token="token")
    iv._client = AuthenticatedClient(
        base_url=BASE_URL,
        token="token",
        httpx_args={"transport": httpx.MockTransport(server.handler)},
    )
    fields = {
        "mime-type": "application/octet-stream",
        "size": len(server.content) if size == -1 else size,
        "data-href": f"{BASE_URL}{BLOB_PATH}",
    }
    if etag:
        fields["etag"] = etag
    return Artifact(iv, id=URN, status=None, **fields)


def _run_in_thread(fn):
    box: dict = {}

    def target():
        try:
            box["result"] = fn()
        except BaseException as e:  # noqa: BLE001 - reported to the test
            box["error"] = e

    t = threading.Thread(target=target, daemon=True)
    t.start()
    return t, box


def _parts(directory) -> list[str]:
    return sorted(p.name for p in directory.glob("*.part"))


def _marker(dest):
    return dest.with_name(f".{dest.name}.ivcap")


def _wait_until(predicate, what="condition"):
    deadline = time.monotonic() + WAIT
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError(f"timed out waiting for {what}")


# ---------------------------------------------------------------------------
# .part file, atomic rename, marker
# ---------------------------------------------------------------------------


def test_final_path_only_appears_when_download_is_complete(tmp_path):
    gate = threading.Event()
    server = FakeServer(gate=gate)
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"

    t, box = _run_in_thread(
        lambda: art.as_local_file(dest, reuse_if_exists=True, chunk_size=1024)
    )
    assert server.started.wait(WAIT)

    # Mid-download: data is in a .part file, the destination does not exist yet.
    assert not dest.exists()
    assert len(_parts(tmp_path)) == 1
    assert not _marker(dest).exists()

    gate.set()
    t.join(WAIT)
    assert "error" not in box, box.get("error")
    assert dest.read_bytes() == CONTENT
    assert _parts(tmp_path) == []
    assert _marker(dest).exists()


def test_marker_records_identity_and_both_etags(tmp_path):
    server = FakeServer()
    art = _make_artifact(server, etag="meta-1")
    dest = tmp_path / "out.bin"

    art.as_local_file(dest)

    marker = json.loads(_marker(dest).read_text())
    assert marker["version"] == 1
    assert marker["urn"] == URN
    assert marker["size"] == len(CONTENT)
    assert marker["artifact_etag"] == "meta-1"
    assert marker["http_etag"] == ETAG
    assert marker["completed_at"]


def test_failed_download_leaves_no_destination_part_or_marker(tmp_path):
    server = FakeServer(drop_after=1000)
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"

    with pytest.raises(httpx.RemoteProtocolError):
        art.as_local_file(dest, max_retries=0, retry_delay=0)

    assert not dest.exists()
    assert not _marker(dest).exists()
    assert _parts(tmp_path) == []


def test_failed_redownload_keeps_previous_file_and_marker(tmp_path):
    dest = tmp_path / "out.bin"
    _make_artifact(FakeServer()).as_local_file(dest)
    before_marker = _marker(dest).read_text()

    failing = _make_artifact(FakeServer(drop_after=1000))
    with pytest.raises(httpx.RemoteProtocolError):
        failing.as_local_file(dest, max_retries=0, retry_delay=0)

    assert dest.read_bytes() == CONTENT
    assert _marker(dest).read_text() == before_marker
    assert _parts(tmp_path) == []


def test_part_file_left_by_a_dead_process_is_ignored_not_resumed(tmp_path):
    stale = tmp_path / "out.bin.99999.deadbeef.part"
    stale.write_bytes(b"half-written junk")
    server = FakeServer()
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"

    art.as_local_file(dest, reuse_if_exists=True)

    assert dest.read_bytes() == CONTENT
    assert "range" not in server.requests[0].headers  # never resumed
    assert stale.read_bytes() == b"half-written junk"  # not ours to delete


# ---------------------------------------------------------------------------
# reuse_if_exists / verify_if_exists
# ---------------------------------------------------------------------------


def test_reuse_skips_download_when_marker_matches(tmp_path):
    server = FakeServer()
    art = _make_artifact(server, etag="meta-1")
    dest = tmp_path / "out.bin"
    art.as_local_file(dest, reuse_if_exists=True)
    inode = dest.stat().st_ino

    again = art.as_local_file(dest, reuse_if_exists=True)

    assert again == dest
    assert len(server.requests) == 1
    assert dest.stat().st_ino == inode


def test_reuse_redownloads_when_artifact_etag_changed(tmp_path):
    server = FakeServer()
    dest = tmp_path / "out.bin"
    _make_artifact(server, etag="meta-1").as_local_file(dest, reuse_if_exists=True)

    _make_artifact(server, etag="meta-2").as_local_file(dest, reuse_if_exists=True)

    assert len(server.requests) == 2
    assert json.loads(_marker(dest).read_text())["artifact_etag"] == "meta-2"


def test_reuse_redownloads_when_file_no_longer_matches_marker(tmp_path):
    server = FakeServer()
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"
    art.as_local_file(dest, reuse_if_exists=True)
    dest.write_bytes(CONTENT[:100])  # truncated behind our back

    art.as_local_file(dest, reuse_if_exists=True)

    assert len(server.requests) == 2
    assert dest.read_bytes() == CONTENT


def test_reuse_with_unknown_artifact_size_uses_marker(tmp_path):
    server = FakeServer()
    art = _make_artifact(server, size=None)
    dest = tmp_path / "out.bin"
    art.as_local_file(dest, reuse_if_exists=True)

    art.as_local_file(dest, reuse_if_exists=True)

    assert len(server.requests) == 1  # old behaviour: always downloaded again
    assert json.loads(_marker(dest).read_text())["size"] == len(CONTENT)


def test_file_without_marker_is_checked_by_size_only(tmp_path):
    server = FakeServer()
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"

    dest.write_bytes(CONTENT)  # e.g. downloaded by an older SDK version
    art.as_local_file(dest, reuse_if_exists=True)
    assert len(server.requests) == 0

    dest.write_bytes(CONTENT[:10])
    art.as_local_file(dest, reuse_if_exists=True)
    assert len(server.requests) == 1
    assert dest.read_bytes() == CONTENT


def test_file_without_marker_and_unknown_size_is_downloaded_again(tmp_path):
    server = FakeServer()
    art = _make_artifact(server, size=None)
    dest = tmp_path / "out.bin"
    dest.write_bytes(CONTENT)

    art.as_local_file(dest, reuse_if_exists=True)

    assert len(server.requests) == 1


def test_verify_false_reuses_any_existing_file(tmp_path):
    server = FakeServer()
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"
    dest.write_bytes(b"anything")

    art.as_local_file(dest, reuse_if_exists=True, verify_if_exists=False)

    assert len(server.requests) == 0
    assert dest.read_bytes() == b"anything"


def test_reuse_false_always_downloads_from_scratch(tmp_path):
    server = FakeServer()
    art = _make_artifact(server)
    dest = tmp_path / "out.bin"
    art.as_local_file(dest)
    art.as_local_file(dest)
    assert len(server.requests) == 2


# ---------------------------------------------------------------------------
# threads
# ---------------------------------------------------------------------------


@pytest.fixture
def follower_spy(monkeypatch):
    """Counts how many threads have started waiting on someone else's download."""
    count = {"n": 0}
    lock = threading.Lock()
    original = artifact_module._wait_for_download

    def spy(*args, **kwargs):
        with lock:
            count["n"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(artifact_module, "_wait_for_download", spy)
    return count


def test_concurrent_callers_share_one_download_and_progress(tmp_path, follower_spy):
    gate = threading.Event()
    server = FakeServer(gate=gate)
    dest = tmp_path / "out.bin"
    progress: list[list[tuple[int, int | None]]] = []

    def call(i):
        calls: list[tuple[int, int | None]] = []
        progress.append(calls)
        art = _make_artifact(server)
        return art.as_local_file(
            dest,
            reuse_if_exists=True,
            chunk_size=1024,
            progress_callback=lambda done, total: calls.append((done, total)),
        )

    leader, leader_box = _run_in_thread(lambda: call(0))
    assert server.started.wait(WAIT)
    followers = [_run_in_thread(lambda i=i: call(i)) for i in (1, 2, 3)]
    _wait_until(lambda: follower_spy["n"] == 3, "3 followers to be waiting")

    gate.set()
    for t, _ in [(leader, leader_box), *followers]:
        t.join(WAIT)

    boxes = [leader_box, *[b for _, b in followers]]
    for b in boxes:
        assert "error" not in b, b.get("error")
        assert b["result"] == dest
    assert len(server.requests) == 1
    assert dest.read_bytes() == CONTENT
    assert len(progress) == 4
    for calls in progress:
        assert calls, "every caller must see progress"
        assert calls[-1] == (len(CONTENT), len(CONTENT))
        done = [d for d, _ in calls]
        assert done == sorted(done)  # never goes backwards
    assert _parts(tmp_path) == []


def test_follower_takes_over_when_leader_fails(tmp_path, follower_spy):
    server = FakeServer(first_status=500)
    dest = tmp_path / "out.bin"

    leader, leader_box = _run_in_thread(
        lambda: _make_artifact(server).as_local_file(dest, reuse_if_exists=True)
    )
    assert server.first_started.wait(WAIT)
    follower, follower_box = _run_in_thread(
        lambda: _make_artifact(server).as_local_file(dest, reuse_if_exists=True)
    )
    _wait_until(lambda: follower_spy["n"] == 1, "follower to be waiting")

    server.first_hold.set()  # leader's request now fails with HTTP 500
    leader.join(WAIT)
    follower.join(WAIT)

    assert isinstance(leader_box.get("error"), httpx.HTTPStatusError)
    assert "error" not in follower_box, follower_box.get("error")
    assert dest.read_bytes() == CONTENT
    assert len(server.requests) == 2
    assert _parts(tmp_path) == []


def test_reuse_false_concurrent_download_warns_and_both_complete(tmp_path, caplog):
    caplog.set_level(logging.WARNING, logger="ivcap_client.artifact")
    gate = threading.Event()
    server = FakeServer(gate=gate)
    dest = tmp_path / "out.bin"

    first, first_box = _run_in_thread(
        lambda: _make_artifact(server).as_local_file(dest, chunk_size=1024)
    )
    assert server.started.wait(WAIT)
    second, second_box = _run_in_thread(
        lambda: _make_artifact(server).as_local_file(dest, chunk_size=1024)
    )
    _wait_until(
        lambda: any("reuse_if_exists=False" in r.getMessage() for r in caplog.records),
        "warning about the concurrent download",
    )

    gate.set()
    first.join(WAIT)
    second.join(WAIT)

    for b in (first_box, second_box):
        assert "error" not in b, b.get("error")
    assert len(server.requests) == 2  # each started from scratch
    assert dest.read_bytes() == CONTENT
    assert _parts(tmp_path) == []
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert any("make no sense" in r.getMessage() for r in warnings)


def test_reuse_false_alone_does_not_warn(tmp_path, caplog):
    caplog.set_level(logging.WARNING, logger="ivcap_client.artifact")
    art = _make_artifact(FakeServer())
    dest = tmp_path / "out.bin"
    art.as_local_file(dest)
    art.as_local_file(dest)  # overwriting an old file is not a concurrency problem
    assert not [r for r in caplog.records if "reuse_if_exists" in r.getMessage()]


# ---------------------------------------------------------------------------
# DataUrlArtifact shares the same implementation
# ---------------------------------------------------------------------------


def test_data_url_artifact_uses_marker_and_reuses(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,aGVsbG8=")
    dest = tmp_path / "hello.txt"

    art.as_local_file(dest, reuse_if_exists=True)
    inode = dest.stat().st_ino
    marker = json.loads(_marker(dest).read_text())
    art.as_local_file(dest, reuse_if_exists=True)

    assert dest.read_bytes() == b"hello"
    assert marker["urn"] == art.urn
    assert marker["size"] == 5
    assert dest.stat().st_ino == inode  # reused, not rewritten
    assert _parts(tmp_path) == []
