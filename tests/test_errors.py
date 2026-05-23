"""Tests for ivcap_client.errors module (UnexpectedStatus)."""

from ivcap_client.errors import UnexpectedStatus


def test_unexpected_status_attributes():
    body = b"something went wrong"
    err = UnexpectedStatus(status_code=503, content=body)
    assert err.status_code == 503
    assert err.content == body
    assert isinstance(err, Exception)


def test_unexpected_status_str_contains_code_and_body():
    err = UnexpectedStatus(status_code=418, content=b"I'm a teapot")
    msg = str(err)
    assert "418" in msg
    assert "teapot" in msg
