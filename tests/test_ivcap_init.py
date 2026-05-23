"""Tests for IVCAP class initialisation and simple factory methods.

No network connection is required – these tests exercise the constructor's
argument/env-var resolution logic and the lightweight factory helpers
(get_service, get_order, get_artifact with a local file path).
"""

import pytest

from ivcap_client.artifact import LocalFileArtifact
from ivcap_client.ivcap import IVCAP
from ivcap_client.order import Order
from ivcap_client.service import Service

# ---------------------------------------------------------------------------
# Constructor – missing/invalid arguments
# ---------------------------------------------------------------------------


def test_ivcap_init_requires_url(monkeypatch):
    monkeypatch.delenv("IVCAP_URL", raising=False)
    monkeypatch.delenv("IVCAP_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="url"):
        IVCAP(token="tok")


def test_ivcap_init_requires_token_for_external_url(monkeypatch):
    monkeypatch.delenv("IVCAP_JWT", raising=False)
    with pytest.raises(ValueError, match="token"):
        IVCAP(url="http://example.com")


# ---------------------------------------------------------------------------
# Constructor – environment-variable resolution
# ---------------------------------------------------------------------------


def test_ivcap_init_url_from_ivcap_url_env(monkeypatch):
    monkeypatch.setenv("IVCAP_URL", "http://from-env.example.com")
    monkeypatch.delenv("IVCAP_BASE_URL", raising=False)
    iv = IVCAP(token="tok")
    assert iv.url == "http://from-env.example.com"


def test_ivcap_init_token_from_env(monkeypatch):
    monkeypatch.setenv("IVCAP_JWT", "env-token")
    monkeypatch.delenv("IVCAP_BASE_URL", raising=False)
    # Should not raise even though no explicit token is passed
    iv = IVCAP(url="http://example.com")
    assert iv._token == "env-token"


def test_ivcap_init_inside_platform_via_base_url_env(monkeypatch):
    """IVCAP_BASE_URL triggers 'inside_platform' mode: no token required."""
    monkeypatch.setenv("IVCAP_BASE_URL", "http://platform.internal")
    monkeypatch.delenv("IVCAP_URL", raising=False)
    monkeypatch.delenv("IVCAP_JWT", raising=False)
    iv = IVCAP()
    assert iv.url == "http://platform.internal"


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------


def test_ivcap_repr():
    iv = IVCAP(url="http://example.com", token="tok")
    assert "http://example.com" in repr(iv)


# ---------------------------------------------------------------------------
# get_service – lightweight (no HTTP, just wraps the id)
# ---------------------------------------------------------------------------


def test_get_service_returns_service_with_id():
    iv = IVCAP(url="http://example.com", token="tok")
    svc = iv.get_service("urn:ivcap:service:test")
    assert isinstance(svc, Service)
    assert svc.id == "urn:ivcap:service:test"


# ---------------------------------------------------------------------------
# get_order – lightweight (no HTTP, just wraps the id)
# ---------------------------------------------------------------------------


def test_get_order_returns_order_with_id():
    iv = IVCAP(url="http://example.com", token="tok")
    order = iv.get_order("urn:ivcap:order:test")
    assert isinstance(order, Order)
    assert order.id == "urn:ivcap:order:test"


# ---------------------------------------------------------------------------
# get_artifact – local-file shortcut (no HTTP needed)
# ---------------------------------------------------------------------------


def test_get_artifact_urn_file_scheme(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello")
    iv = IVCAP(url="http://example.com", token="tok")
    art = iv.get_artifact(f"urn:file://{f}")
    assert isinstance(art, LocalFileArtifact)


def test_get_artifact_bare_file_scheme(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello")
    iv = IVCAP(url="http://example.com", token="tok")
    art = iv.get_artifact(f"file://{f}")
    assert isinstance(art, LocalFileArtifact)


# ---------------------------------------------------------------------------
# artifact_for_file – returns None when file not yet uploaded
# ---------------------------------------------------------------------------


def test_artifact_for_file_returns_none_when_not_uploaded(tmp_path):
    f = tmp_path / "new.txt"
    f.write_text("data")
    iv = IVCAP(url="http://example.com", token="tok")
    result = iv.artifact_for_file(str(f))
    assert result is None
