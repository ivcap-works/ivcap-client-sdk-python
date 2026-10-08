import base64
import os
import tempfile

import httpx
import pytest

from ivcap_client import artifact
from ivcap_client.artifact import Artifact
from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import ArtifactTooLargeForDataUrlError
from ivcap_client.ivcap import IVCAP


def test_safepath_smoke():
    safepath = artifact.SafePath()
    assert safepath is not None


def test_safepath_unlink_does_not_delete_file():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "x")
        with open(p, "w") as f:
            f.write("hello")

        sp = artifact.SafePath(p)
        sp.unlink()

        # should still exist because SafePath.unlink is a no-op
        assert os.path.exists(p)


def test_CMPath_():
    with tempfile.TemporaryDirectory() as td:
        with artifact.CMPath(os.path.join(td, "x")) as x_file:
            with open(x_file, "w") as f:
                f.write("hello")
        # now outside of the context manager, the CMPath should be cleaned up
        assert "x" not in os.listdir(td)


# ---------------------------------------------------------------------------
# Artifact.as_data_url
# ---------------------------------------------------------------------------


def _make_mocked_artifact(content: bytes, *, mime_type: str, size: int | None = None):
    """Build an Artifact backed by an httpx.MockTransport that serves `content`."""
    base_url = "http://test"
    blob_path = "/1/artifacts/urn:ivcap:artifact:abc/blob"

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == blob_path
        return httpx.Response(200, content=content)

    transport = httpx.MockTransport(handler)
    iv = IVCAP(url=base_url, token="token")
    iv._client = AuthenticatedClient(
        base_url=base_url, token="token", httpx_args={"transport": transport}
    )

    art = Artifact(
        iv,
        id="urn:ivcap:artifact:abc",
        status=None,
        **{
            "mime-type": mime_type,
            "size": size if size is not None else len(content),
            "data-href": f"{base_url}{blob_path}",
        },
    )
    return art


def test_as_data_url_returns_expected_data_url():
    content = b"Hello, World!"
    art = _make_mocked_artifact(content, mime_type="text/plain")

    url = art.as_data_url()

    expected = f"data:text/plain;base64,{base64.b64encode(content).decode()}"
    assert url == expected


def test_as_data_url_raises_when_known_size_exceeds_max_length():
    """Should fail fast (without downloading) when the known `size` already
    guarantees the encoded data URL exceeds max_length."""
    art = _make_mocked_artifact(b"x" * 1000, mime_type="application/octet-stream")

    with pytest.raises(ArtifactTooLargeForDataUrlError) as exc_info:
        art.as_data_url(max_length=10)

    err = exc_info.value
    assert err.artifact_id == "urn:ivcap:artifact:abc"
    assert err.content_size == 1000
    assert err.max_length == 10
    assert "exceeds max_length=10" in str(err)


def test_as_data_url_raises_when_actual_content_exceeds_max_length():
    """When `size` is unknown/unset, the check happens after downloading."""
    content = b"x" * 100
    art = _make_mocked_artifact(content, mime_type="text/plain", size=None)
    art.size = None  # simulate unknown size, forcing the post-download check

    with pytest.raises(ArtifactTooLargeForDataUrlError):
        art.as_data_url(max_length=20)


def test_as_data_url_default_max_length_is_512():
    # 384 raw bytes -> ~512+ base64 chars -> should just barely fail by default
    content = b"x" * 384
    art = _make_mocked_artifact(content, mime_type="text/plain")

    with pytest.raises(ArtifactTooLargeForDataUrlError):
        art.as_data_url()
