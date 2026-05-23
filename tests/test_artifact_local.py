"""Tests for LocalFileArtifact, ProxyFile, and upload_artifact input validation.

All tests here are offline – no network, no IVCAP server.
"""

import io

import pytest

from ivcap_client.artifact import LocalFileArtifact, ProxyFile, upload_artifact

# ---------------------------------------------------------------------------
# LocalFileArtifact
# ---------------------------------------------------------------------------


def test_local_file_artifact_basic_attributes(tmp_path):
    f = tmp_path / "test.txt"
    content = "hello world"
    f.write_text(content)
    art = LocalFileArtifact(f"urn:file://{f}")
    assert art.name == "test.txt"
    assert art.size == len(content.encode())


def test_local_file_artifact_via_file_scheme(tmp_path):
    """'file://' prefix (without 'urn:') is also accepted."""
    f = tmp_path / "test.txt"
    f.write_text("hi")
    art = LocalFileArtifact(f"file://{f}")
    # id is normalised to urn:file://...
    assert "file://" in art.id


def test_local_file_artifact_mime_type_for_known_extension(tmp_path):
    f = tmp_path / "image.png"
    f.write_bytes(b"\x89PNG\r\n\x1a\n")
    art = LocalFileArtifact(f"urn:file://{f}")
    assert "image" in art.mime_type


def test_local_file_artifact_mime_type_fallback_for_unknown_extension(tmp_path):
    f = tmp_path / "data.xyzabc123"
    f.write_bytes(b"whatever")
    art = LocalFileArtifact(f"urn:file://{f}")
    assert art.mime_type == "application/octet-stream"


def test_local_file_artifact_refresh_returns_self(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("content")
    art = LocalFileArtifact(f"urn:file://{f}")
    assert art.refresh() is art


def test_local_file_artifact_missing_file_raises(tmp_path):
    nonexistent = tmp_path / "ghost.txt"
    with pytest.raises(ValueError, match="does not exist"):
        LocalFileArtifact(f"urn:file://{nonexistent}")


def test_local_file_artifact_open_returns_readable(tmp_path):
    f = tmp_path / "readable.txt"
    f.write_text("hello\nworld\n")
    art = LocalFileArtifact(f"urn:file://{f}")
    with art.open() as fh:
        text = fh.read()
    assert "hello" in text


def test_local_file_artifact_as_local_file_returns_existing_path(tmp_path):
    f = tmp_path / "f.txt"
    f.write_text("data")
    art = LocalFileArtifact(f"urn:file://{f}")
    p = art.as_local_file()
    assert p.exists()


# ---------------------------------------------------------------------------
# ProxyFile
# ---------------------------------------------------------------------------


def test_proxy_file_read():
    pf = ProxyFile(io.BytesIO(b"hello world"))
    assert pf.read() == b"hello world"


def test_proxy_file_context_manager_closes():
    buf = io.BytesIO(b"data")
    with ProxyFile(buf) as pf:
        data = pf.read()
    assert data == b"data"
    assert pf.closed


def test_proxy_file_closed_raises_on_read():
    pf = ProxyFile(io.BytesIO(b"data"))
    pf.close()
    with pytest.raises(ValueError, match="closed"):
        pf.read()


def test_proxy_file_seek_and_tell():
    pf = ProxyFile(io.BytesIO(b"abcdef"))
    pf.seek(3)
    assert pf.tell() == 3
    assert pf.read() == b"def"


def test_proxy_file_readline():
    pf = ProxyFile(io.BytesIO(b"line1\nline2\n"))
    assert pf.readline() == b"line1\n"


def test_proxy_file_readlines():
    pf = ProxyFile(io.BytesIO(b"line1\nline2\n"))
    lines = pf.readlines()
    assert len(lines) == 2


def test_proxy_file_closed_raises_on_readline():
    pf = ProxyFile(io.BytesIO(b"data"))
    pf.close()
    with pytest.raises(ValueError, match="closed"):
        pf.readline()


def test_proxy_file_closed_raises_on_seek():
    pf = ProxyFile(io.BytesIO(b"data"))
    pf.close()
    with pytest.raises(ValueError, match="closed"):
        pf.seek(0)


def test_proxy_file_closed_raises_on_tell():
    pf = ProxyFile(io.BytesIO(b"data"))
    pf.close()
    with pytest.raises(ValueError, match="closed"):
        pf.tell()


def test_proxy_file_double_close_is_safe():
    pf = ProxyFile(io.BytesIO(b"data"))
    pf.close()
    pf.close()  # second close must not raise
    assert pf.closed


# ---------------------------------------------------------------------------
# upload_artifact – input validation (no network needed)
# ---------------------------------------------------------------------------


def test_upload_artifact_requires_file_or_stream():
    """Calling with neither file_path nor io_stream must raise ValueError."""
    from unittest.mock import MagicMock

    ivcap = MagicMock()
    with pytest.raises(ValueError, match="file_path"):
        upload_artifact(ivcap)


def test_upload_artifact_nonexistent_file_raises():
    from unittest.mock import MagicMock

    ivcap = MagicMock()
    with pytest.raises(ValueError, match="doesn't exist"):
        upload_artifact(ivcap, file_path="/absolutely/no/such/file/xyz.txt")
