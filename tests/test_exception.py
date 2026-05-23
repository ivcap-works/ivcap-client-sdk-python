"""Tests for ivcap_client.exception module.

These cover the exception hierarchy, __str__ formatting, and the
_safe_decode_content helper – all pure logic that doesn't need a network.
"""


from ivcap_client.exception import (
    AmbiguousRequest,
    IvcapApiError,
    IvcapError,
    MissingParameterValue,
    NotAuthorizedException,
    ResourceNotFound,
    _safe_decode_content,
)

# ---------------------------------------------------------------------------
# IvcapApiError.__str__
# ---------------------------------------------------------------------------


def test_ivcap_api_error_str_minimal():
    err = IvcapApiError(operation="list", status_code=500)
    assert str(err) == "list failed with HTTP 500"


def test_ivcap_api_error_str_with_url():
    err = IvcapApiError(operation="list", status_code=404, url="http://example.com/api")
    s = str(err)
    assert "list failed with HTTP 404" in s
    assert "http://example.com/api" in s


def test_ivcap_api_error_str_with_bytes_content():
    err = IvcapApiError(
        operation="upload", status_code=400, content=b"bad request body"
    )
    s = str(err)
    assert "bad request body" in s


def test_ivcap_api_error_str_with_string_content():
    err = IvcapApiError(operation="search", status_code=422, content="invalid query")
    s = str(err)
    assert "invalid query" in s


def test_ivcap_api_error_str_url_and_content():
    """Both url and content should appear in the message."""
    err = IvcapApiError(
        operation="get",
        status_code=403,
        content=b"forbidden",
        url="http://api.test/resource",
    )
    s = str(err)
    assert "403" in s
    assert "forbidden" in s
    assert "api.test" in s


def test_ivcap_api_error_is_ivcap_error():
    err = IvcapApiError(operation="x", status_code=500)
    assert isinstance(err, IvcapError)
    assert isinstance(err, Exception)


# ---------------------------------------------------------------------------
# NotAuthorizedException
# ---------------------------------------------------------------------------


def test_not_authorized_default_status_code():
    err = NotAuthorizedException(operation="read")
    assert err.status_code == 401
    assert isinstance(err, IvcapApiError)


def test_not_authorized_custom_403():
    err = NotAuthorizedException(operation="write", status_code=403)
    assert err.status_code == 403


def test_not_authorized_str_includes_operation():
    err = NotAuthorizedException(operation="list_services")
    assert "list_services" in str(err)


# ---------------------------------------------------------------------------
# ResourceNotFound
# ---------------------------------------------------------------------------


def test_resource_not_found_message_contains_resource():
    err = ResourceNotFound("urn:ivcap:service:missing")
    assert "urn:ivcap:service:missing" in str(err)


def test_resource_not_found_resource_attribute():
    err = ResourceNotFound("my-resource")
    assert err.resource == "my-resource"
    assert isinstance(err, Exception)


# ---------------------------------------------------------------------------
# AmbiguousRequest
# ---------------------------------------------------------------------------


def test_ambiguous_request_message():
    err = AmbiguousRequest("too many matches for 'foo'")
    assert "foo" in str(err)
    assert isinstance(err, Exception)


# ---------------------------------------------------------------------------
# MissingParameterValue
# ---------------------------------------------------------------------------


def test_missing_parameter_value_is_exception():
    err = MissingParameterValue("param x is required")
    assert isinstance(err, Exception)


# ---------------------------------------------------------------------------
# _safe_decode_content
# ---------------------------------------------------------------------------


def test_safe_decode_content_none_returns_empty():
    assert _safe_decode_content(None) == ""


def test_safe_decode_content_bytes():
    assert _safe_decode_content(b"hello") == "hello"


def test_safe_decode_content_str():
    assert _safe_decode_content("world") == "world"


def test_safe_decode_content_truncates_long_bytes():
    long_content = b"a" * 5000
    result = _safe_decode_content(long_content, limit=100)
    # Should be exactly limit chars + the ellipsis character
    assert "…" in result
    assert len(result) <= 110  # a little slack for the ellipsis


def test_safe_decode_content_short_content_not_truncated():
    content = b"short"
    result = _safe_decode_content(content, limit=100)
    assert result == "short"
    assert "…" not in result


def test_safe_decode_content_invalid_utf8_survives():
    # \xff is not valid UTF-8; should use replacement char, not raise
    result = _safe_decode_content(b"\xff\xfe")
    assert isinstance(result, str)
    assert len(result) > 0
