"""Tests for LocalIVCAP — fully offline, no network required."""

import io

import pytest

from ivcap_client.artifact import LocalFileArtifact, LocalIVCAP
from ivcap_client.exception import ResourceNotFound
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
    dest = tmp_path / "out" / "artifacts" / "result.txt"
    assert dest.exists()
    assert dest.read_text() == "hello"


def test_upload_artifact_file_path_urn_is_absolute(tmp_path):
    src = tmp_path / "f.txt"
    src.write_text("data")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    artifact = ivcap.upload_artifact(name="f.txt", file_path=str(src))

    assert artifact.id.startswith("urn:file://")
    # The id must encode an absolute path inside the artifacts/ subdir
    assert str(tmp_path / "out" / "artifacts") in artifact.id


def test_upload_artifact_creates_nested_dirs(tmp_path):
    src = tmp_path / "data.csv"
    src.write_text("a,b\n1,2\n")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    ivcap.upload_artifact(name="deep/nested/data.csv", file_path=str(src))

    assert (tmp_path / "out" / "artifacts" / "deep" / "nested" / "data.csv").exists()


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

    dest = tmp_path / "out" / "artifacts" / "blob.bin"
    assert dest.exists()
    assert dest.read_bytes() == data
    assert isinstance(artifact, LocalFileArtifact)


def test_upload_artifact_text_stream(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")

    ivcap.upload_artifact(
        name="notes.txt",
        io_stream=io.StringIO("line1\nline2\n"),
        content_type="text/plain",
    )

    dest = tmp_path / "out" / "artifacts" / "notes.txt"
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
    # File should exist under base_dir/artifacts/
    p = tmp_path / "out" / "artifacts"
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


# ---------------------------------------------------------------------------
# get_artifact / register_artifact — platform artifact URN mapping
# ---------------------------------------------------------------------------


def test_register_artifact_resolves_via_get_artifact(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(b"platform content")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    urn = "urn:ivcap:artifact:11111111-1111-1111-1111-111111111111"

    ivcap.register_artifact(urn, f)
    artifact = ivcap.get_artifact(urn)

    assert isinstance(artifact, LocalFileArtifact)
    assert artifact.name == "data.bin"


def test_register_artifact_does_not_write_sidecar_file(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(b"content")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    urn = "urn:ivcap:artifact:22222222-2222-2222-2222-222222222222"

    ivcap.register_artifact(urn, f)

    # the mapping is purely in-memory — no sidecar file is ever created
    assert not (tmp_path / ".ivcap-data.bin.txt").exists()
    # a fresh LocalIVCAP instance (no in-memory cache) can't resolve it
    fresh = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(ResourceNotFound):
        fresh.get_artifact(urn)


def test_register_artifact_raises_for_missing_file(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(ValueError, match="does not exist"):
        ivcap.register_artifact("urn:ivcap:artifact:x", tmp_path / "ghost.bin")


def test_get_artifact_unknown_platform_urn_raises(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(ResourceNotFound):
        ivcap.get_artifact("urn:ivcap:artifact:99999999-9999-9999-9999-999999999999")


def test_get_artifact_resolves_via_upload_sidecar(tmp_path):
    """A file previously uploaded via the *platform* IVCAP.upload_artifact
    (which writes a ``.ivcap-<name>.txt`` sidecar next to the source file)
    can be resolved by a LocalIVCAP instance that scans base_dir for it,
    even without an explicit register_artifact() call."""
    from ivcap_client.artifact import mark_file_already_uploaded

    base = tmp_path / "out"
    base.mkdir()
    f = base / "shared.csv"
    f.write_text("a,b\n1,2\n")
    urn = "urn:ivcap:artifact:33333333-3333-3333-3333-333333333333"
    mark_file_already_uploaded(urn, str(f))

    ivcap = LocalIVCAP(base_dir=base)
    artifact = ivcap.get_artifact(urn)

    assert isinstance(artifact, LocalFileArtifact)
    assert artifact.name == "shared.csv"


def test_get_artifact_sidecar_scan_rejects_stale_content(tmp_path):
    """If the file content no longer matches the recorded md5, the sidecar
    match is ignored (stale/edited fixture)."""
    from ivcap_client.artifact import mark_file_already_uploaded

    base = tmp_path / "out"
    base.mkdir()
    f = base / "stale.csv"
    f.write_text("original")
    urn = "urn:ivcap:artifact:44444444-4444-4444-4444-444444444444"
    mark_file_already_uploaded(urn, str(f))

    # file content changes after being recorded
    f.write_text("edited")

    ivcap = LocalIVCAP(base_dir=base)
    with pytest.raises(ResourceNotFound):
        ivcap.get_artifact(urn)


# ---------------------------------------------------------------------------
# get_artifact / register_artifact — mime-type propagation
# ---------------------------------------------------------------------------


def test_register_artifact_with_explicit_mime_type_overrides_guess(tmp_path):
    # Extension-less file — mimetypes.guess_type() would return None/octet-stream
    f = tmp_path / "payload"
    f.write_bytes(b"{}")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    urn = "urn:ivcap:artifact:55555555-5555-5555-5555-555555555555"

    ivcap.register_artifact(urn, f, mime_type="application/json")
    artifact = ivcap.get_artifact(urn)

    assert artifact.mime_type == "application/json"


def test_register_artifact_without_mime_type_falls_back_to_guess(tmp_path):
    f = tmp_path / "data.csv"
    f.write_text("a,b\n")
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    urn = "urn:ivcap:artifact:66666666-6666-6666-6666-666666666666"

    ivcap.register_artifact(urn, f)
    artifact = ivcap.get_artifact(urn)

    assert artifact.mime_type == "text/csv"


def test_get_artifact_sidecar_scan_recovers_mime_type(tmp_path):
    """mark_file_already_uploaded(..., mime_type=...) records the real
    mime-type in the sidecar, and the scan-based resolution path in
    LocalIVCAP picks it up — even for a renamed/extension-less fixture
    file where guessing from the name would be wrong."""
    from ivcap_client.artifact import mark_file_already_uploaded

    base = tmp_path / "out"
    base.mkdir()
    f = base / "fixture_no_ext"
    f.write_bytes(b"\x89PNG\r\n")
    urn = "urn:ivcap:artifact:77777777-7777-7777-7777-777777777777"
    mark_file_already_uploaded(urn, str(f), mime_type="image/png")

    ivcap = LocalIVCAP(base_dir=base)
    artifact = ivcap.get_artifact(urn)

    assert artifact.mime_type == "image/png"


def test_sidecar_without_mime_type_field_still_works(tmp_path):
    """Backward compatibility: sidecars written before mime-type support was
    added (``<md5>|<urn>`` only, no trailing field) continue to resolve."""
    from ivcap_client.artifact import mark_file_already_uploaded

    base = tmp_path / "out"
    base.mkdir()
    f = base / "legacy.csv"
    f.write_text("a,b\n1,2\n")
    urn = "urn:ivcap:artifact:88888888-8888-8888-8888-888888888888"
    mark_file_already_uploaded(urn, str(f))  # no mime_type kwarg → 2-field sidecar

    ivcap = LocalIVCAP(base_dir=base)
    artifact = ivcap.get_artifact(urn)

    assert artifact.name == "legacy.csv"
    # falls back to guessing from the extension since none was recorded
    assert artifact.mime_type == "text/csv"
