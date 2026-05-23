import json

import pytest
from pydantic import ValidationError

from ivcap_client.utils import model_from_json_schema


def load_schema():
    with open("tests/schema_with_defs.json") as f:
        return json.load(f)


def test_model_from_json_schema_accepts_object():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    # Should accept a dict for "call"
    data = {
        "$schema": "urn:sd:schema:ai-tester.request.1",
        "call": {"method": "GET", "url": "http://ivcap.local/1/services2"},
    }
    m = Model(**data)
    assert m.call.method == "GET"
    assert m.call.url == "http://ivcap.local/1/services2"


def test_model_from_json_schema_accepts_null():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    data = {"$schema": "urn:sd:schema:ai-tester.request.1", "call": None}
    m = Model(**data)
    assert m.call is None


def test_model_from_json_schema_rejects_string_for_object():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    data = {"$schema": "urn:sd:schema:ai-tester.request.1", "call": "not a dict"}
    with pytest.raises(ValidationError):
        Model(**data)


# ---------------------------------------------------------------------------
# Additional coverage for model_from_json_schema code paths
# ---------------------------------------------------------------------------


def test_model_from_json_schema_primitive_types():
    """integer, number, and boolean field types are all handled."""
    schema = {
        "type": "object",
        "properties": {
            "count": {"type": "integer"},
            "ratio": {"type": "number"},
            "flag": {"type": "boolean"},
            "label": {"type": "string"},
        },
        "required": ["count", "ratio", "flag", "label"],
    }
    Model = model_from_json_schema(schema, "PrimitivesModel")
    m = Model(count=3, ratio=1.5, flag=True, label="hello")
    assert m.count == 3
    assert m.ratio == 1.5
    assert m.flag is True
    assert m.label == "hello"


def test_model_from_json_schema_array_field():
    """Array properties are parsed into List[<item_type>]."""
    schema = {
        "type": "object",
        "properties": {
            "tags": {
                "type": "array",
                "items": {"type": "string"},
            }
        },
        "required": ["tags"],
    }
    Model = model_from_json_schema(schema, "ArrayModel")
    m = Model(tags=["a", "b", "c"])
    assert m.tags == ["a", "b", "c"]


def test_model_from_json_schema_union_no_null():
    """anyOf with multiple non-null types should produce a Union field."""
    schema = {
        "type": "object",
        "properties": {
            "value": {
                "anyOf": [{"type": "string"}, {"type": "integer"}],
            }
        },
        "required": ["value"],
    }
    Model = model_from_json_schema(schema, "UnionModel")
    # Both types must be accepted
    m_str = Model(value="hello")
    assert m_str.value == "hello"
    m_int = Model(value=42)
    assert m_int.value == 42


def test_model_from_json_schema_non_local_ref_raises():
    """$ref pointing outside the document must raise NotImplementedError."""
    schema = {
        "type": "object",
        "properties": {
            "item": {"$ref": "https://external.example.com/schema#/Foo"},
        },
    }
    with pytest.raises(NotImplementedError):
        Model = model_from_json_schema(schema, "ExternalRefModel")
        # The error is raised during field resolution, which happens at class
        # creation time in model_from_json_schema.
        _ = Model
