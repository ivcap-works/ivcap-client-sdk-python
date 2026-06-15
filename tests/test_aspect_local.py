"""Tests for LocalIVCAP aspect support — fully offline, no network required."""

import json

import pytest

from ivcap_client.artifact import LocalAspect, LocalIVCAP
from ivcap_client.exception import MissingParameterValue, ResourceNotFound

# ---------------------------------------------------------------------------
# add_aspect — happy path
# ---------------------------------------------------------------------------


def test_add_aspect_returns_local_aspect(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.add_aspect(
        entity="urn:ivcap:artifact:test",
        aspect={"$schema": "urn:test:schema:tag.1", "tag": "hello"},
    )
    assert isinstance(aspect, LocalAspect)


def test_add_aspect_urn_format(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.add_aspect(
        entity="urn:ivcap:artifact:test",
        aspect={"$schema": "urn:test:schema:tag.1", "tag": "hello"},
    )
    assert aspect.id.startswith("urn:ivcap:aspect:")
    uuid_part = aspect.id[len("urn:ivcap:aspect:") :]
    assert len(uuid_part) == 36  # standard UUID length


def test_add_aspect_fields(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    body = {"$schema": "urn:test:schema:tag.1", "tag": "marine"}
    aspect = ivcap.add_aspect(entity="urn:ivcap:artifact:abc", aspect=body)

    assert aspect.entity == "urn:ivcap:artifact:abc"
    assert aspect.schema == "urn:test:schema:tag.1"
    assert aspect.content == body
    assert aspect.aspect == body
    assert aspect.valid_from is not None
    assert aspect.valid_to is None


def test_add_aspect_explicit_schema_overrides_body(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    body = {"$schema": "urn:test:schema:ignored.1", "val": 1}
    aspect = ivcap.add_aspect(
        entity="urn:e:1",
        aspect=body,
        schema="urn:test:schema:explicit.1",
    )
    assert aspect.schema == "urn:test:schema:explicit.1"


def test_add_aspect_creates_json_file(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.add_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:x.1", "x": 42},
    )
    uuid_part = aspect.id[len("urn:ivcap:aspect:") :]
    expected_file = tmp_path / "out" / "aspects" / f"{uuid_part}.json"
    assert expected_file.exists()

    record = json.loads(expected_file.read_text())
    assert record["id"] == aspect.id
    assert record["entity"] == "urn:e:1"
    assert record["schema"] == "urn:test:schema:x.1"
    assert record["content"]["x"] == 42


def test_add_aspect_multiple_calls_create_separate_files(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    body = {"$schema": "urn:test:schema:tag.1", "tag": "a"}

    a1 = ivcap.add_aspect(entity="urn:e:1", aspect=body)
    a2 = ivcap.add_aspect(entity="urn:e:1", aspect=body)

    assert a1.id != a2.id
    aspects_dir = tmp_path / "out" / "aspects"
    files = list(aspects_dir.glob("*.json"))
    assert len(files) == 2


def test_add_aspect_policy_silently_ignored(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    # Should not raise even though local mode has no policy support
    aspect = ivcap.add_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:x.1"},
        policy="urn:ivcap:policy:open",
    )
    assert isinstance(aspect, LocalAspect)


# ---------------------------------------------------------------------------
# add_aspect — validation errors
# ---------------------------------------------------------------------------


def test_add_aspect_missing_entity_raises(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(MissingParameterValue, match="entity"):
        ivcap.add_aspect(entity="", aspect={"$schema": "urn:s:1"})


def test_add_aspect_missing_schema_raises(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(MissingParameterValue, match="schema"):
        ivcap.add_aspect(entity="urn:e:1", aspect={"no_schema": True})


# ---------------------------------------------------------------------------
# update_aspect — delegates to add_aspect
# ---------------------------------------------------------------------------


def test_update_aspect_returns_local_aspect(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.update_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:tag.1", "tag": "updated"},
    )
    assert isinstance(aspect, LocalAspect)
    assert aspect.content["tag"] == "updated"


def test_update_aspect_creates_new_file_each_time(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    body = {"$schema": "urn:test:schema:tag.1", "tag": "v1"}
    ivcap.update_aspect(entity="urn:e:1", aspect=body)
    ivcap.update_aspect(entity="urn:e:1", aspect={**body, "tag": "v2"})

    aspects_dir = tmp_path / "out" / "aspects"
    assert len(list(aspects_dir.glob("*.json"))) == 2


# ---------------------------------------------------------------------------
# get_aspect — round-trip
# ---------------------------------------------------------------------------


def test_get_aspect_by_urn(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    created = ivcap.add_aspect(
        entity="urn:ivcap:artifact:xyz",
        aspect={"$schema": "urn:test:schema:tag.1", "tag": "roundtrip"},
    )

    retrieved = ivcap.get_aspect(created.id)

    assert isinstance(retrieved, LocalAspect)
    assert retrieved.id == created.id
    assert retrieved.entity == created.entity
    assert retrieved.schema == created.schema
    assert retrieved.content["tag"] == "roundtrip"
    assert retrieved.valid_from is not None


def test_get_aspect_by_bare_uuid(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    created = ivcap.add_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:x.1", "v": 7},
    )
    bare_uuid = created.id[len("urn:ivcap:aspect:") :]
    retrieved = ivcap.get_aspect(bare_uuid)
    assert retrieved.id == created.id


def test_get_aspect_not_found_raises(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    with pytest.raises(ResourceNotFound):
        ivcap.get_aspect("urn:ivcap:aspect:00000000-0000-0000-0000-000000000000")


# ---------------------------------------------------------------------------
# LocalAspect properties
# ---------------------------------------------------------------------------


def test_local_aspect_urn_property(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.add_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:x.1"},
    )
    assert aspect.urn == aspect.id


def test_local_aspect_repr(tmp_path):
    ivcap = LocalIVCAP(base_dir=tmp_path / "out")
    aspect = ivcap.add_aspect(
        entity="urn:e:1",
        aspect={"$schema": "urn:test:schema:x.1"},
    )
    r = repr(aspect)
    assert "LocalAspect" in r
    assert aspect.id in r
