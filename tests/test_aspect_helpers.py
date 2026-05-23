"""Tests for _add_update_aspect input validation (no network required).

The validation logic (missing entity, missing schema, invalid policy URI)
all fires before the actual HTTP call is made, so we can use a MagicMock
for the IVCAP instance.
"""

from unittest.mock import MagicMock

import pytest

from ivcap_client.aspect import _add_update_aspect
from ivcap_client.exception import MissingParameterValue


def _ivcap():
    return MagicMock()


def test_add_aspect_missing_entity_raises():
    with pytest.raises(MissingParameterValue, match="entity"):
        _add_update_aspect(_ivcap(), False, "", {"$schema": "urn:test:schema"})


def test_add_aspect_none_entity_raises():
    with pytest.raises(MissingParameterValue, match="entity"):
        _add_update_aspect(_ivcap(), False, None, {"$schema": "urn:test:schema"})


def test_add_aspect_missing_schema_in_body_raises():
    """Neither an explicit schema nor '$schema' in the body → error."""
    with pytest.raises(MissingParameterValue, match="schema"):
        _add_update_aspect(_ivcap(), False, "urn:entity:1", {"key": "value"})


def test_add_aspect_schema_taken_from_body_no_missing_param():
    """When '$schema' is present in the body, MissingParameterValue must NOT
    be raised.  We verify this by confirming the error that actually surfaces
    is NOT a MissingParameterValue (the MagicMock HTTP call fails with its own
    error further down the stack, which is fine)."""
    ivcap = _ivcap()
    with pytest.raises(Exception) as exc_info:
        _add_update_aspect(
            ivcap, False, "urn:entity:1", {"$schema": "urn:test:schema", "x": 1}
        )
    assert not isinstance(exc_info.value, MissingParameterValue)


def test_add_aspect_invalid_policy_raises():
    """A policy that doesn't start with 'urn:ivcap:policy:' must be rejected."""
    with pytest.raises(ValueError, match="policy"):
        _add_update_aspect(
            _ivcap(),
            False,
            "urn:entity:1",
            {"$schema": "urn:test:schema"},
            policy="not-a-valid-policy-urn",
        )


def test_update_aspect_missing_entity_raises():
    """is_update=True follows the same validation path."""
    with pytest.raises(MissingParameterValue, match="entity"):
        _add_update_aspect(_ivcap(), True, "", {"$schema": "urn:test:schema"})
