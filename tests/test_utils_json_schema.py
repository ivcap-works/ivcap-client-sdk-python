import json
import pytest
from pydantic import ValidationError

from ivcap_client.utils import model_from_json_schema

def load_schema():
    with open("tests/schema_with_defs.json", "r") as f:
        return json.load(f)

def test_model_from_json_schema_accepts_object():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    # Should accept a dict for "call"
    data = {
        "$schema": "urn:sd:schema:ai-tester.request.1",
        "call": {
            "method": "GET",
            "url": "http://ivcap.local/1/services2"
        }
    }
    m = Model(**data)
    assert m.call.method == "GET"
    assert m.call.url == "http://ivcap.local/1/services2"

def test_model_from_json_schema_accepts_null():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    data = {
        "$schema": "urn:sd:schema:ai-tester.request.1",
        "call": None
    }
    m = Model(**data)
    assert m.call is None

def test_model_from_json_schema_rejects_string_for_object():
    schema = load_schema()
    Model = model_from_json_schema(schema, "RequestModel")
    data = {
        "$schema": "urn:sd:schema:ai-tester.request.1",
        "call": "not a dict"
    }
    with pytest.raises(ValidationError):
        Model(**data)
