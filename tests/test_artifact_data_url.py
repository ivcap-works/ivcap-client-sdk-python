"""Tests for DataUrlArtifact and the RFC 2397 'data:' URL support in get_artifact.

All tests here are offline – no network, no IVCAP server.
"""

import base64
import io
import tarfile

import pytest

from ivcap_client.artifact import (
    DataUrlArtifact,
    _parse_data_url,
    is_data_url,
)
from ivcap_client.ivcap import IVCAP, LocalIVCAP

# ---------------------------------------------------------------------------
# is_data_url
# ---------------------------------------------------------------------------


def test_is_data_url_true_for_data_scheme():
    assert is_data_url("data:text/plain;base64,aGVsbG8=")


def test_is_data_url_true_for_urn_data_scheme():
    assert is_data_url("urn:data:text/plain;base64,aGVsbG8=")


@pytest.mark.parametrize(
    "value",
    [
        "urn:ivcap:artifact:some-uuid",
        "file:///tmp/f.txt",
        "urn:file:///tmp/f.txt",
        "",
    ],
)
def test_is_data_url_false_for_other_schemes(value):
    assert not is_data_url(value)


# ---------------------------------------------------------------------------
# _parse_data_url
# ---------------------------------------------------------------------------


def test_parse_data_url_base64():
    mime, charset, content = _parse_data_url("data:text/plain;base64,aGVsbG8=")
    assert mime == "text/plain"
    assert charset is None
    assert content == b"hello"


def test_parse_data_url_percent_encoded_text():
    mime, charset, content = _parse_data_url("data:text/plain,Hello%2C%20World!")
    assert mime == "text/plain"
    assert content == b"Hello, World!"


def test_parse_data_url_default_mime_type():
    mime, _, content = _parse_data_url("data:,plain%20text")
    assert mime == "text/plain"
    assert content == b"plain text"


def test_parse_data_url_with_charset_param():
    mime, charset, content = _parse_data_url(
        "data:text/plain;charset=utf-8;base64,aGVsbG8="
    )
    assert mime == "text/plain"
    assert charset == "utf-8"
    assert content == b"hello"


def test_parse_data_url_tolerates_missing_base64_padding():
    # 'aGVsbG8' (no padding) still decodes to b"hello"
    mime, _, content = _parse_data_url("data:text/plain;base64,aGVsbG8")
    assert content == b"hello"


def test_parse_data_url_malformed_raises():
    with pytest.raises(ValueError):
        _parse_data_url("not-a-data-url")


def test_parse_data_url_urn_prefixed_form():
    mime, _, content = _parse_data_url("urn:data:text/plain;base64,aGVsbG8=")
    assert mime == "text/plain"
    assert content == b"hello"


# ---------------------------------------------------------------------------
# DataUrlArtifact
# ---------------------------------------------------------------------------


def test_data_url_artifact_basic_attributes():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art.mime_type == "text/plain"
    assert art.size == len(b"Hello, World!")
    assert art.id == "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
    assert art.urn == art.id


def test_data_url_artifact_open_reads_decoded_bytes():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    with art.open() as f:
        assert f.read() == b"Hello, World!"


def test_data_url_artifact_as_stream_reassembles_full_content():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert b"".join(art.as_stream()) == b"Hello, World!"


def test_data_url_artifact_as_stream_small_chunk_size():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    chunks = list(art.as_stream(chunk_size=3))
    assert all(len(c) <= 3 for c in chunks)
    assert b"".join(chunks) == b"Hello, World!"


def test_data_url_artifact_as_local_file_temp(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    with art.as_local_file() as path:
        assert path.read_bytes() == b"Hello, World!"


def test_data_url_artifact_as_local_file_explicit_path(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "nested" / "out.txt"
    path = art.as_local_file(dest)
    assert path == dest
    assert dest.read_bytes() == b"Hello, World!"


def test_data_url_artifact_as_local_file_reuse_if_exists_skips_matching_size(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "out.txt"
    dest.write_bytes(b"XXXXXXXXXXXXX")  # same 13-byte size, different content
    path = art.as_local_file(dest, reuse_if_exists=True)
    assert path == dest
    assert dest.read_bytes() == b"XXXXXXXXXXXXX"


def test_data_url_artifact_as_local_file_reuse_verifies_size_by_default(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "out.txt"
    dest.write_bytes(b"cached")  # size mismatch -> re-download
    art.as_local_file(dest, reuse_if_exists=True)
    assert dest.read_bytes() == b"Hello, World!"


def test_data_url_artifact_as_local_file_reuse_without_verify_skips_download(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "out.txt"
    dest.write_bytes(b"cached")
    art.as_local_file(dest, reuse_if_exists=True, verify_if_exists=False)
    assert dest.read_bytes() == b"cached"


def test_data_url_artifact_as_local_file_overwrites_by_default(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "out.txt"
    dest.write_bytes(b"cached")
    art.as_local_file(dest)
    assert dest.read_bytes() == b"Hello, World!"


def test_data_url_artifact_as_local_file_explicit_path_context_manager_keeps_file(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    dest = tmp_path / "keep.txt"
    with art.as_local_file(dest) as path:
        assert path.read_bytes() == b"Hello, World!"
    assert dest.exists()
    assert dest.read_bytes() == b"Hello, World!"


def test_data_url_artifact_etag_is_stable_md5():
    art1 = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    art2 = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art1.etag == art2.etag


def test_data_url_artifact_status_is_ready():
    from ivcap_client.models.artifact_status_rt_status import ArtifactStatusRTStatus

    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art.status.status == ArtifactStatusRTStatus.READY


def test_data_url_artifact_refresh_returns_self():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art.refresh() is art


def test_data_url_artifact_repr():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert "DataUrlArtifact" in repr(art)


def test_data_url_artifact_as_data_url_roundtrips_to_plain_data_form():
    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art.as_data_url() == "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="


def test_data_url_artifact_as_data_url_normalises_urn_prefix_to_plain_data():
    art = DataUrlArtifact("urn:data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    # as_data_url() always returns the canonical 'data:' form, even though
    # .id/.urn preserve the original 'urn:data:' form.
    assert art.as_data_url() == "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
    assert art.id == "urn:data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="


def test_data_url_artifact_as_data_url_raises_when_too_large():
    from ivcap_client.exception import ArtifactTooLargeForDataUrlError

    art = DataUrlArtifact("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    with pytest.raises(ArtifactTooLargeForDataUrlError):
        art.as_data_url(max_length=10)


def test_data_url_artifact_accepts_urn_data_prefix():
    art = DataUrlArtifact("urn:data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert art.mime_type == "text/plain"
    assert art._content == b"Hello, World!"
    # id/urn preserve the original 'urn:data:' form passed in
    assert art.id == "urn:data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
    assert art.urn == art.id


# ---------------------------------------------------------------------------
# DataUrlArtifact — tar support
# ---------------------------------------------------------------------------


def _make_tar_gz_data_url(filename: str, content: bytes) -> str:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        info = tarfile.TarInfo(name=filename)
        info.size = len(content)
        tar.addfile(info, io.BytesIO(content))
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:application/gzip;base64,{b64}"


def test_data_url_artifact_is_tar_file_true_for_tar_mime():
    url = _make_tar_gz_data_url("hello.txt", b"hello tar")
    art = DataUrlArtifact(url)
    assert art.is_tar_file


def test_data_url_artifact_is_tar_file_false_for_plain_text():
    art = DataUrlArtifact("data:text/plain;base64,aGVsbG8=")
    assert not art.is_tar_file


def test_data_url_artifact_untar_extracts_files(tmp_path):
    url = _make_tar_gz_data_url("hello.txt", b"hello tar")
    art = DataUrlArtifact(url)
    dest = art.untar(tmp_path / "extracted")
    assert (dest / "hello.txt").read_bytes() == b"hello tar"


def test_data_url_artifact_untar_raises_for_non_tar(tmp_path):
    art = DataUrlArtifact("data:text/plain;base64,aGVsbG8=")
    with pytest.raises(ValueError, match="tar archive"):
        art.untar(tmp_path / "extracted")


# ---------------------------------------------------------------------------
# IVCAP.get_artifact / LocalIVCAP.get_artifact — data URL dispatch
# ---------------------------------------------------------------------------


def test_ivcap_get_artifact_dispatches_data_url():
    iv = IVCAP(url="http://example.com", token="tok")
    art = iv.get_artifact("data:text/plain;base64,SGVsbG8=")
    assert isinstance(art, DataUrlArtifact)


def test_local_ivcap_get_artifact_dispatches_data_url(tmp_path):
    iv = LocalIVCAP(base_dir=tmp_path)
    art = iv.get_artifact("data:text/plain;base64,SGVsbG8=")
    assert isinstance(art, DataUrlArtifact)


def test_ivcap_get_artifact_dispatches_urn_data_url():
    iv = IVCAP(url="http://example.com", token="tok")
    art = iv.get_artifact("urn:data:text/plain;base64,SGVsbG8=")
    assert isinstance(art, DataUrlArtifact)


def test_local_ivcap_get_artifact_dispatches_urn_data_url(tmp_path):
    iv = LocalIVCAP(base_dir=tmp_path)
    art = iv.get_artifact("urn:data:text/plain;base64,SGVsbG8=")
    assert isinstance(art, DataUrlArtifact)
