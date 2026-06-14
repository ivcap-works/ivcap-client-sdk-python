"""Tests for LocalIVCAP — fully offline, no network required."""

import io

import pytest

from ivcap_client.artifact import LocalFileArtifact, LocalIVCAP
from ivcap_client.ivcap import IVCAP


# ---------------------------------------------------------------------------
# LocalIVCAP construction
# ---------------------------------------------------------------------------


def test_local_ivcap_default_base_dir():
    ivcap = LocalIVCAP()
    assert str(ivcap.base_dir) == "ivcap-artifacts"


def test_local_ivcap_custom_base_dir(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "my-artifacts")
    assert ivcap.base_dir == tmp_path / "my-artifacts"


def test_local_ivcap_repr(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path)
    assert "LocalIVCAP" in repr(ivcap)


# ---------------------------------------------------------------------------
# IVCAP.local() factory
# ---------------------------------------------------------------------------


def test_ivcap_local_factory_returns_local_ivcap(tmp_path):
    ivcap = IVCAP.local(base_dir=str(tmp_path / "arts"))
    assert isinstance(ivcap, LocalIVCAP)


def test_ivcap_local_factory_uses_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("IVCAP_LOCAL_DIR", str(tmp_path / "env-arts"))
    ivcap = IVCAP.local()
    assert str(ivcap.base_dir) == str(tmp_path / "env-arts")


def test_ivcap_local_factory_explicit_overrides_env_var(tmp_path, monkeypatch):
    monkeypatch.setenv("IVCAP_LOCAL_DIR", str(tmp_path / "env-arts"))
    ivcap = IVCAP.local(base_dir=str(tmp_path / "explicit"))
    assert str(ivcap.base_dir) == str(tmp_path / "explicit")


def test_ivcap_local_factory_default_without_env(monkeypatch):
    monkeypatch.delenv("IVCAP_LOCAL_DIR", raising=False)
    ivcap = IVCAP.local()
    assert str(ivcap.base_dir) == "ivcap-artifacts"


# ---------------------------------------------------------------------------
# upload_artifact via file_path
# ---------------------------------------------------------------------------


def test_upload_artifact_file_path_creates_file(tmp_path):
    src = tmp_path / "src.txt"
    src.write_text("hello")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(name="result.txt", file_path=str(src))

    assert isinstance(artifact, LocalFileArtifact)
    dest = tmp_path / "out" / "result.txt"
    assert dest.exists()
    assert dest.read_text() == "hello"


def test_upload_artifact_file_path_urn_is_absolute(tmp_path):
    src = tmp_path / "f.txt"
    src.write_text("data")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(name="f.txt", file_path=str(src))

    assert artifact.id.startswith("urn:file://")
    # The id must encode an absolute path
    assert str(tmp_path) in artifact.id


def test_upload_artifact_creates_nested_dirs(tmp_path):
    src = tmp_path / "data.csv"
    src.write_text("a,b\n1,2\n")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    ivcap.upload_artifact(name="deep/nested/data.csv", file_path=str(src))

    assert (tmp_path / "out" / "deep" / "nested" / "data.csv").exists()


# ---------------------------------------------------------------------------
# upload_artifact via io_stream
# ---------------------------------------------------------------------------


def test_upload_artifact_bytes_stream(tmp_path):
    data = b"\x00\x01\x02binary"
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(
        name="blob.bin",
        io_stream=io.BytesIO(data),
        content_type="application/octet-stream",
    )

    dest = tmp_path / "out" / "blob.bin"
    assert dest.exists()
    assert dest.read_bytes() == data
    assert isinstance(artifact, LocalFileArtifact)


def test_upload_artifact_text_stream(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(
        name="notes.txt",
        io_stream=io.StringIO("line1\nline2\n"),
        content_type="text/plain",
    )

    dest = tmp_path / "out" / "notes.txt"
    assert dest.exists()
    assert "line1" in dest.read_text()


# ---------------------------------------------------------------------------
# Auto-naming when name is None
# ---------------------------------------------------------------------------


def test_upload_artifact_auto_name_when_none(tmp_path):
    src = tmp_path / "x.py"
    src.write_text("# code")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(file_path=str(src))

    # Extension should be preserved
    assert artifact.id.endswith(".py")
    # File should exist under base_dir
    p = tmp_path / "out"
    files = list(p.glob("*.py"))
    assert len(files) == 1


def test_upload_artifact_auto_name_stream_has_no_ext(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    artifact = ivcap.upload_artifact(io_stream=io.BytesIO(b"raw"))
    # No extension — UUID only
    from pathlib import Path

    p = Path(artifact.id[len("urn:file://") :])
    assert p.exists()


# ---------------------------------------------------------------------------
# upload_artifact — ignored parameters don't cause errors
# ---------------------------------------------------------------------------


def test_upload_artifact_ignores_collection_and_policy(tmp_path):
    src = tmp_path / "f.txt"
    src.write_text("x")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    # Should not raise
    artifact = ivcap.upload_artifact(
        name="f.txt",
        file_path=str(src),
        collection="urn:ivcap:collection:some-uuid",
        policy="urn:ivcap:policy:some-policy",
    )
    assert isinstance(artifact, LocalFileArtifact)


def test_upload_artifact_extra_kwargs_ignored(tmp_path):
    src = tmp_path / "f.txt"
    src.write_text("x")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(
        name="f.txt",
        file_path=str(src),
        chunk_size=1024,
        retries=3,
        retry_delay=10,
        force_upload=True,
    )
    assert isinstance(artifact, LocalFileArtifact)


# ---------------------------------------------------------------------------
# upload_artifact — error cases
# ---------------------------------------------------------------------------


def test_upload_artifact_requires_file_or_stream(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(ValueError, match="file_path"):
        ivcap.upload_artifact(name="f.txt")


# ---------------------------------------------------------------------------
# get_artifact
# ---------------------------------------------------------------------------


def test_get_artifact_returns_local_file_artifact(tmp_path):
    f = tmp_path / "existing.txt"
    f.write_text("content")
    ivcap = LocalIVCAP(base_dir=tmp_path)

    artifact = ivcap.get_artifact(f"urn:file://{f}")
    assert isinstance(artifact, LocalFileArtifact)
    assert artifact.name == "existing.txt"


def test_get_artifact_file_scheme(tmp_path):
    f = tmp_path / "existing.txt"
    f.write_text("content")
    ivcap = LocalIVCAP(base_dir=tmp_path)

    artifact = ivcap.get_artifact(f"file://{f}")
    assert isinstance(artifact, LocalFileArtifact)


# ---------------------------------------------------------------------------
# Round-trip: upload then open
# ---------------------------------------------------------------------------


def test_upload_then_open_round_trip(tmp_path):
    text = "round-trip content\n"
    src = tmp_path / "input.txt"
    src.write_text(text)
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(name="output.txt", file_path=str(src))

    with artifact.open() as fh:
        result = fh.read()
    assert "round-trip" in result
