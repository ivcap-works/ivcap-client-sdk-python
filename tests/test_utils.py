"""Tests for ivcap_client.utils module.

Covers the small helper functions and process_error – all unit-testable
without a live HTTP connection.
"""

from types import SimpleNamespace

import pytest

from ivcap_client.exception import IvcapApiError, NotAuthorizedException
from ivcap_client.types import UNSET, Unset
from ivcap_client.utils import (
    Links,
    _unset,
    _unset_bool,
    _wrap,
    process_error,
    set_page,
)

# ---------------------------------------------------------------------------
# _wrap
# ---------------------------------------------------------------------------


def test_wrap_none_returns_unset():
    result = _wrap(None)
    assert isinstance(result, Unset)


def test_wrap_value_passes_through():
    assert _wrap(42) == 42
    assert _wrap("hello") == "hello"
    # False is a value, not None – must NOT become UNSET
    assert _wrap(False) is False


# ---------------------------------------------------------------------------
# _unset
# ---------------------------------------------------------------------------


def test_unset_with_unset_sentinel_returns_none():
    assert _unset(UNSET) is None


def test_unset_with_empty_string_returns_none():
    assert _unset("") is None


def test_unset_with_value_passes_through():
    assert _unset("hello") == "hello"
    assert _unset(42) == 42
    assert _unset(True) is True


# ---------------------------------------------------------------------------
# _unset_bool
# ---------------------------------------------------------------------------


def test_unset_bool_with_unset_returns_false():
    assert _unset_bool(UNSET) is False


def test_unset_bool_with_none_returns_false():
    assert _unset_bool(None) is False


def test_unset_bool_with_true_returns_true():
    assert _unset_bool(True) is True


def test_unset_bool_with_false_returns_false():
    # explicit False should stay False (not converted to None/default)
    assert _unset_bool(False) is False


# ---------------------------------------------------------------------------
# process_error
# ---------------------------------------------------------------------------


def _fake_response(
    status_code: int, content: bytes = b"error", url: str = "http://test/api"
):
    """Build a minimal response-like object that process_error can inspect."""
    req = SimpleNamespace(url=url)
    return SimpleNamespace(
        status_code=status_code,
        content=content,
        request=req,
        headers={},
    )


def test_process_error_401_raises_not_authorized():
    r = _fake_response(401, b"unauthorised")
    with pytest.raises(NotAuthorizedException) as exc_info:
        process_error("get_service", r, verbose=False)
    assert exc_info.value.status_code == 401
    assert exc_info.value.operation == "get_service"


def test_process_error_403_raises_not_authorized():
    r = _fake_response(403, b"forbidden")
    with pytest.raises(NotAuthorizedException) as exc_info:
        process_error("list_services", r, verbose=False)
    assert exc_info.value.status_code == 403


def test_process_error_500_raises_ivcap_api_error_not_not_authorized():
    r = _fake_response(500, b"server error")
    with pytest.raises(IvcapApiError) as exc_info:
        process_error("search", r, verbose=False)
    assert exc_info.value.status_code == 500
    # Must NOT be promoted to NotAuthorizedException
    assert not isinstance(exc_info.value, NotAuthorizedException)


def test_process_error_url_appears_in_exception():
    r = _fake_response(404, url="http://example.com/1/services")
    with pytest.raises(IvcapApiError) as exc_info:
        process_error("get", r, verbose=False)
    assert "example.com" in str(exc_info.value)


# ---------------------------------------------------------------------------
# set_page
# ---------------------------------------------------------------------------


def test_set_page_valid():
    token = set_page("http://example.com/1/services?page=abc123")
    assert token == "abc123"


def test_set_page_invalid_query_raises():
    with pytest.raises(Exception, match="unexpected"):
        set_page("http://example.com/1/services?limit=10")


def test_set_page_handles_url_with_trailing_content():
    # page= at the start of the query string must be returned verbatim
    token = set_page("http://host/path?page=token-xyz-789")
    assert token == "token-xyz-789"


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------


def _link(rel: str, href: str):
    return SimpleNamespace(rel=rel, href=href)


def test_links_parses_all_three():
    links = Links(
        [
            _link("self", "http://example.com/self"),
            _link("next", "http://example.com/next?page=xyz"),
            _link("first", "http://example.com/first"),
        ]
    )
    assert links.this == "http://example.com/self"
    assert links.next == "http://example.com/next?page=xyz"
    assert links.first == "http://example.com/first"


def test_links_missing_next_is_none():
    links = Links([_link("self", "http://example.com/self")])
    assert links.this == "http://example.com/self"
    assert links.next is None
    assert links.first is None


def test_links_empty_list():
    links = Links([])
    assert links.this is None
    assert links.next is None
    assert links.first is None
