"""Tests for the collection module.

All validation logic fires before any real HTTP call is made, so we can use
MagicMock/respx for network-level stubs.  Tests that exercise the actual HTTP
path mock the underlying ``aspect_list`` / ``_add_update_aspect`` helpers to
keep the suite self-contained (no real IVCAP deployment required).
"""

from __future__ import annotations

import datetime
from http import HTTPStatus
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from ivcap_client.collection import (
    COLLECTION_ITEM_SCHEMA,
    COLLECTION_SCHEMA,
    Collection,
    CollectionItem,
    add_item_to_collection,
    create_collection,
    get_collection,
    list_collections,
    remove_item_from_collection,
    retract_collection,
)
from ivcap_client.exception import MissingParameterValue, ResourceNotFound
from ivcap_client.types import UNSET

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COLL_URN = "urn:ivcap:collection:11111111-1111-1111-1111-111111111111"
ITEM_URN = "urn:ivcap:artifact:22222222-2222-2222-2222-222222222222"
ASPECT_URN = "urn:ivcap:aspect:33333333-3333-3333-3333-333333333333"


def _ivcap():
    """Return a minimal MagicMock that satisfies Collection / helper signatures."""
    mock = MagicMock()
    mock._client = MagicMock()
    return mock


def _make_aspect_list_rt(items=None, links=None):
    """Build a minimal AspectListRT-like SimpleNamespace."""
    result = SimpleNamespace()
    result.items = items or []
    result.links = links or []
    return result


def _make_list_item_rt(
    entity=COLL_URN,
    schema=COLLECTION_SCHEMA,
    content_dict=None,
    valid_from=None,
):
    """Build a minimal AspectListItemRT-like SimpleNamespace."""
    item = SimpleNamespace()
    item.id = ASPECT_URN
    item.entity = entity
    item.schema = schema
    item.valid_from = valid_from or datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
    item.valid_to = UNSET
    item.additional_properties = {}

    if content_dict is not None:
        content = SimpleNamespace()
        content.to_dict = lambda: content_dict
        item.content = content
    else:
        item.content = UNSET

    return item


def _make_ok_response(parsed):
    """Return a Response-like SimpleNamespace with status 200."""
    r = SimpleNamespace()
    r.status_code = HTTPStatus(200)
    r.parsed = parsed
    return r


def _make_created_response(parsed):
    """Return a Response-like SimpleNamespace with status 201."""
    r = SimpleNamespace()
    r.status_code = HTTPStatus(201)
    r.parsed = parsed
    return r


# ---------------------------------------------------------------------------
# CollectionItem — unit tests (pure Python, no I/O)
# ---------------------------------------------------------------------------


class TestCollectionItem:
    def test_basic_creation(self):
        ci = CollectionItem(
            id=ASPECT_URN,
            collection=COLL_URN,
            item=ITEM_URN,
        )
        assert ci.id == ASPECT_URN
        assert ci.collection == COLL_URN
        assert ci.item == ITEM_URN
        assert ci.valid_from is None
        assert ci.valid_to is None

    def test_urn_property_aliases_item(self):
        ci = CollectionItem(id="a", collection="b", item=ITEM_URN)
        assert ci.urn == ITEM_URN

    def test_repr(self):
        ci = CollectionItem(id="a", collection=COLL_URN, item=ITEM_URN)
        r = repr(ci)
        assert "CollectionItem" in r
        assert ITEM_URN in r

    def test_unset_valid_times_become_none(self):
        ci = CollectionItem(
            id="a", collection="b", item="c", valid_from=UNSET, valid_to=UNSET
        )
        assert ci.valid_from is None
        assert ci.valid_to is None


# ---------------------------------------------------------------------------
# Collection — unit tests (pure Python, no I/O)
# ---------------------------------------------------------------------------


class TestCollection:
    def test_basic_creation(self):
        coll = Collection(_ivcap(), urn=COLL_URN, name="Test")
        assert coll.urn == COLL_URN
        assert coll.name == "Test"
        assert coll.description is None
        assert coll.valid_to is None

    def test_id_property_aliases_urn(self):
        coll = Collection(_ivcap(), urn=COLL_URN, name="X")
        assert coll.id == COLL_URN

    def test_missing_ivcap_raises(self):
        with pytest.raises(ValueError, match="ivcap"):
            Collection(None, urn=COLL_URN, name="Test")

    def test_entity_kwarg_sets_urn(self):
        """'entity' is an accepted alias for 'urn' (used when built from an aspect)."""
        coll = Collection(_ivcap(), entity=COLL_URN, name="From aspect")
        assert coll.urn == COLL_URN

    def test_repr(self):
        coll = Collection(_ivcap(), urn=COLL_URN, name="Ocean Survey")
        r = repr(coll)
        assert "Collection" in r
        assert "Ocean Survey" in r

    def test_update_with_datetime_string(self):
        coll = Collection(
            _ivcap(),
            urn=COLL_URN,
            name="T",
            valid_from="2024-06-01T00:00:00+00:00",
        )
        assert isinstance(coll.valid_from, datetime.datetime)

    def test_update_with_datetime_object(self):
        dt = datetime.datetime(2024, 6, 1, tzinfo=datetime.UTC)
        coll = Collection(_ivcap(), urn=COLL_URN, name="T", valid_from=dt)
        assert coll.valid_from == dt

    def test_unset_valid_times_become_none(self):
        coll = Collection(
            _ivcap(), urn=COLL_URN, name="T", valid_from=UNSET, valid_to=UNSET
        )
        assert coll.valid_from is None
        assert coll.valid_to is None


# ---------------------------------------------------------------------------
# create_collection — input validation (no network)
# ---------------------------------------------------------------------------


class TestCreateCollectionValidation:
    def test_missing_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="URN"):
            create_collection(_ivcap(), "", "My Collection")

    def test_none_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="URN"):
            create_collection(_ivcap(), None, "My Collection")

    def test_missing_name_raises(self):
        with pytest.raises(MissingParameterValue, match="name"):
            create_collection(_ivcap(), COLL_URN, "")

    def test_none_name_raises(self):
        with pytest.raises(MissingParameterValue, match="name"):
            create_collection(_ivcap(), COLL_URN, None)

    def test_new_collection_uses_post(self):
        """create_collection should use POST (is_update=False) when the collection does not exist yet."""
        ivcap = _ivcap()
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN, entity=COLL_URN, schema=COLLECTION_SCHEMA, content={}
        )
        # aspect_list returns empty → collection does not exist → expect POST
        empty_response = _make_ok_response(_make_aspect_list_rt(items=[]))
        with (
            patch(
                "ivcap_client.collection.aspect_list.sync_detailed",
                return_value=empty_response,
            ),
            patch(
                "ivcap_client.collection._add_update_aspect",
                return_value=mock_aspect,
            ) as mock_aua,
        ):
            coll = create_collection(
                ivcap, COLL_URN, "Ocean Survey", description="CTD casts"
            )

        # Must use POST (is_update=False) for a brand-new collection
        args = mock_aua.call_args
        assert args[0][1] is False, "expected is_update=False (POST) for new collection"
        assert args[0][2] == COLL_URN
        assert args[1]["schema"] == COLLECTION_SCHEMA

        assert isinstance(coll, Collection)
        assert coll.urn == COLL_URN
        assert coll.name == "Ocean Survey"
        assert coll.description == "CTD casts"

    def test_existing_collection_uses_put(self):
        """create_collection should use PUT (is_update=True) when the collection already exists."""
        ivcap = _ivcap()
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN, entity=COLL_URN, schema=COLLECTION_SCHEMA, content={}
        )
        # aspect_list returns an item → collection exists → expect PUT
        existing_item = _make_list_item_rt()
        existing_response = _make_ok_response(
            _make_aspect_list_rt(items=[existing_item])
        )
        with (
            patch(
                "ivcap_client.collection.aspect_list.sync_detailed",
                return_value=existing_response,
            ),
            patch(
                "ivcap_client.collection._add_update_aspect",
                return_value=mock_aspect,
            ) as mock_aua,
        ):
            coll = create_collection(ivcap, COLL_URN, "Ocean Survey Updated")

        # Must use PUT (is_update=True) for an existing collection
        args = mock_aua.call_args
        assert args[0][1] is True, (
            "expected is_update=True (PUT) for existing collection"
        )
        assert args[0][2] == COLL_URN
        assert args[1]["schema"] == COLLECTION_SCHEMA

        assert isinstance(coll, Collection)
        assert coll.urn == COLL_URN


# ---------------------------------------------------------------------------
# get_collection — logic tests
# ---------------------------------------------------------------------------


class TestGetCollection:
    def test_raises_resource_not_found_when_no_items(self):
        ivcap = _ivcap()
        empty_response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_response,
        ):
            with pytest.raises(ResourceNotFound):
                get_collection(ivcap, COLL_URN)

    def test_returns_collection_from_aspect(self):
        ivcap = _ivcap()
        list_item = _make_list_item_rt(
            content_dict={"name": "Ocean Survey", "description": "CTD casts"}
        )
        response = _make_ok_response(_make_aspect_list_rt(items=[list_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ):
            coll = get_collection(ivcap, COLL_URN)

        assert isinstance(coll, Collection)
        assert coll.urn == COLL_URN
        assert coll.name == "Ocean Survey"
        assert coll.description == "CTD casts"

    def test_returns_collection_without_description(self):
        ivcap = _ivcap()
        list_item = _make_list_item_rt(content_dict={"name": "Simple"})
        response = _make_ok_response(_make_aspect_list_rt(items=[list_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ):
            coll = get_collection(ivcap, COLL_URN)

        assert coll.name == "Simple"
        assert coll.description is None

    def test_queries_correct_schema_and_entity(self):
        ivcap = _ivcap()
        list_item = _make_list_item_rt(content_dict={"name": "X"})
        response = _make_ok_response(_make_aspect_list_rt(items=[list_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ) as mock_list:
            get_collection(ivcap, COLL_URN)

        call_kwargs = mock_list.call_args[1]
        assert call_kwargs["entity"] == COLL_URN
        assert call_kwargs["schema"] == COLLECTION_SCHEMA
        assert call_kwargs["include_content"] is True


# ---------------------------------------------------------------------------
# list_collections — logic tests
# ---------------------------------------------------------------------------


class TestListCollections:
    def test_returns_iterator(self):
        ivcap = _ivcap()
        list_item = _make_list_item_rt(content_dict={"name": "Survey 1"})
        response = _make_ok_response(_make_aspect_list_rt(items=[list_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ):
            result = list(list_collections(ivcap, limit=5))

        assert len(result) == 1
        assert isinstance(result[0], Collection)
        assert result[0].name == "Survey 1"

    def test_name_filter_builds_content_path(self):
        ivcap = _ivcap()
        response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ) as mock_list:
            list(list_collections(ivcap, name_filter='== "Ocean Survey"', limit=5))

        call_kwargs = mock_list.call_args[1]
        assert "$.name" in call_kwargs["content_path"]
        assert "Ocean Survey" in call_kwargs["content_path"]

    def test_no_name_filter_omits_content_path(self):
        ivcap = _ivcap()
        response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ) as mock_list:
            list(list_collections(ivcap, limit=5))

        call_kwargs = mock_list.call_args[1]
        # content_path should be UNSET (falsy) when no filter is provided
        from ivcap_client.types import Unset

        assert isinstance(call_kwargs.get("content_path"), Unset)

    def test_always_queries_collection_schema(self):
        ivcap = _ivcap()
        response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ) as mock_list:
            list(list_collections(ivcap))

        call_kwargs = mock_list.call_args[1]
        assert call_kwargs["schema"] == COLLECTION_SCHEMA


# ---------------------------------------------------------------------------
# add_item_to_collection — logic tests
# ---------------------------------------------------------------------------


class TestAddItemToCollection:
    def test_missing_collection_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            add_item_to_collection(_ivcap(), "", ITEM_URN)

    def test_none_collection_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            add_item_to_collection(_ivcap(), None, ITEM_URN)

    def test_missing_item_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="item"):
            add_item_to_collection(_ivcap(), COLL_URN, "")

    def test_none_item_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="item"):
            add_item_to_collection(_ivcap(), COLL_URN, None)

    def test_returns_none_when_already_member(self):
        """If the dedup check finds an existing record, must return None."""
        ivcap = _ivcap()
        existing_item = _make_list_item_rt(schema=COLLECTION_ITEM_SCHEMA)
        dedup_response = _make_ok_response(_make_aspect_list_rt(items=[existing_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=dedup_response,
        ):
            result = add_item_to_collection(ivcap, COLL_URN, ITEM_URN)

        assert result is None

    def test_creates_aspect_when_not_member(self):
        """If the dedup check finds nothing, a new membership aspect is POSTed."""
        ivcap = _ivcap()
        empty_dedup = _make_ok_response(_make_aspect_list_rt(items=[]))
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN,
            entity=COLL_URN,
            schema=COLLECTION_ITEM_SCHEMA,
            content={"collection": COLL_URN, "item": ITEM_URN},
        )

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_dedup,
        ):
            with patch(
                "ivcap_client.collection._add_update_aspect",
                return_value=mock_aspect,
            ) as mock_aua:
                result = add_item_to_collection(ivcap, COLL_URN, ITEM_URN)

        # Must use POST (is_update=False)
        args = mock_aua.call_args
        assert args[0][1] is False, "expected is_update=False for POST semantics"
        assert args[1]["schema"] == COLLECTION_ITEM_SCHEMA

        assert isinstance(result, CollectionItem)
        assert result.collection == COLL_URN
        assert result.item == ITEM_URN

    def test_dedup_check_uses_jsonpath_filter(self):
        """The dedup query must use a content_path JSONPath filter containing the item URN."""
        ivcap = _ivcap()
        empty_dedup = _make_ok_response(_make_aspect_list_rt(items=[]))
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN, entity=COLL_URN, schema=COLLECTION_ITEM_SCHEMA, content={}
        )

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_dedup,
        ) as mock_list:
            with patch(
                "ivcap_client.collection._add_update_aspect", return_value=mock_aspect
            ):
                add_item_to_collection(ivcap, COLL_URN, ITEM_URN)

        call_kwargs = mock_list.call_args[1]
        assert ITEM_URN in call_kwargs["content_path"], (
            "dedup query must embed the item URN in a JSONPath content_path filter"
        )
        assert call_kwargs["schema"] == COLLECTION_ITEM_SCHEMA
        assert call_kwargs["entity"] == COLL_URN

    def test_dedup_check_does_not_request_content(self):
        """The dedup query should set include_content=False to minimise data transfer."""
        ivcap = _ivcap()
        empty_dedup = _make_ok_response(_make_aspect_list_rt(items=[]))
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN, entity=COLL_URN, schema=COLLECTION_ITEM_SCHEMA, content={}
        )

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_dedup,
        ) as mock_list:
            with patch(
                "ivcap_client.collection._add_update_aspect", return_value=mock_aspect
            ):
                add_item_to_collection(ivcap, COLL_URN, ITEM_URN)

        call_kwargs = mock_list.call_args[1]
        assert call_kwargs.get("include_content") is False

    def test_proceeds_to_post_when_dedup_check_fails_with_5xx(self):
        """If the dedup check returns 5xx (e.g. EOF / content_path not supported),
        add_item_to_collection must fall through to POST rather than raising."""
        ivcap = _ivcap()
        # Simulate a 500 response from the dedup check
        error_response = SimpleNamespace()
        error_response.status_code = HTTPStatus(500)
        error_response.parsed = None
        mock_aspect = SimpleNamespace(
            id=ASPECT_URN, entity=COLL_URN, schema=COLLECTION_ITEM_SCHEMA, content={}
        )

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=error_response,
        ):
            with patch(
                "ivcap_client.collection._add_update_aspect",
                return_value=mock_aspect,
            ) as mock_aua:
                result = add_item_to_collection(ivcap, COLL_URN, ITEM_URN)

        # Must have fallen through to POST despite the 500 dedup check
        mock_aua.assert_called_once()
        args = mock_aua.call_args
        assert args[0][1] is False, "should still use POST (is_update=False)"
        assert isinstance(result, CollectionItem)
        assert result.item == ITEM_URN


# ---------------------------------------------------------------------------
# Collection.add_item — delegates to add_item_to_collection
# ---------------------------------------------------------------------------


class TestCollectionAddItem:
    def test_delegates_to_module_function(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")

        with patch(
            "ivcap_client.collection.add_item_to_collection",
            return_value=None,
        ) as mock_fn:
            result = coll.add_item(ITEM_URN)

        mock_fn.assert_called_once_with(ivcap, COLL_URN, ITEM_URN, policy=None)
        assert result is None

    def test_delegates_policy_to_module_function(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")
        policy = "urn:ivcap:policy:open"

        with patch(
            "ivcap_client.collection.add_item_to_collection",
            return_value=None,
        ) as mock_fn:
            coll.add_item(ITEM_URN, policy=policy)

        mock_fn.assert_called_once_with(ivcap, COLL_URN, ITEM_URN, policy=policy)


# ---------------------------------------------------------------------------
# Collection.items — returns CollectionItemIter
# ---------------------------------------------------------------------------


class TestCollectionItems:
    def test_items_queries_correct_schema_and_entity(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")

        item_rt = _make_list_item_rt(
            schema=COLLECTION_ITEM_SCHEMA,
            content_dict={"collection": COLL_URN, "item": ITEM_URN},
        )
        response = _make_ok_response(_make_aspect_list_rt(items=[item_rt]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=response,
        ) as mock_list:
            results = list(coll.items(limit=5))

        call_kwargs = mock_list.call_args[1]
        assert call_kwargs["entity"] == COLL_URN
        assert call_kwargs["schema"] == COLLECTION_ITEM_SCHEMA
        assert call_kwargs["include_content"] is True

        assert len(results) == 1
        ci = results[0]
        assert isinstance(ci, CollectionItem)
        assert ci.item == ITEM_URN
        assert ci.collection == COLL_URN


# ---------------------------------------------------------------------------
# remove_item_from_collection — logic tests
# ---------------------------------------------------------------------------


class TestRemoveItemFromCollection:
    def test_missing_collection_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            remove_item_from_collection(_ivcap(), "", ITEM_URN)

    def test_none_collection_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            remove_item_from_collection(_ivcap(), None, ITEM_URN)

    def test_missing_item_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="item"):
            remove_item_from_collection(_ivcap(), COLL_URN, "")

    def test_none_item_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="item"):
            remove_item_from_collection(_ivcap(), COLL_URN, None)

    def test_returns_false_when_not_a_member(self):
        """If the find query returns no items, return False (skip silently)."""
        ivcap = _ivcap()
        empty_response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_response,
        ):
            result = remove_item_from_collection(ivcap, COLL_URN, ITEM_URN)

        assert result is False

    def test_retracts_aspect_when_member(self):
        """If the find query returns an aspect, retract it and return True."""
        ivcap = _ivcap()
        existing_item = _make_list_item_rt(schema=COLLECTION_ITEM_SCHEMA)
        find_response = _make_ok_response(_make_aspect_list_rt(items=[existing_item]))

        retract_response = SimpleNamespace()
        retract_response.status_code = HTTPStatus(204)
        retract_response.parsed = None

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=find_response,
        ):
            with patch(
                "ivcap_client.collection.aspect_retract.sync_detailed",
                return_value=retract_response,
            ) as mock_retract:
                result = remove_item_from_collection(ivcap, COLL_URN, ITEM_URN)

        assert result is True
        mock_retract.assert_called_once_with(ASPECT_URN, client=ivcap._client)

    def test_find_query_uses_jsonpath_filter(self):
        """The find query must embed the item URN in a JSONPath content_path filter."""
        ivcap = _ivcap()
        empty_response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_response,
        ) as mock_list:
            remove_item_from_collection(ivcap, COLL_URN, ITEM_URN)

        call_kwargs = mock_list.call_args[1]
        assert ITEM_URN in call_kwargs["content_path"]
        assert call_kwargs["schema"] == COLLECTION_ITEM_SCHEMA
        assert call_kwargs["entity"] == COLL_URN
        assert call_kwargs.get("include_content") is False

    def test_find_query_limit_is_1(self):
        """Efficiency: the find query must use limit=1."""
        ivcap = _ivcap()
        empty_response = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty_response,
        ) as mock_list:
            remove_item_from_collection(ivcap, COLL_URN, ITEM_URN)

        call_kwargs = mock_list.call_args[1]
        assert call_kwargs.get("limit") == 1


# ---------------------------------------------------------------------------
# Collection.remove_item — delegates to remove_item_from_collection
# ---------------------------------------------------------------------------


class TestCollectionRemoveItem:
    def test_returns_false_when_not_a_member(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")

        with patch(
            "ivcap_client.collection.remove_item_from_collection",
            return_value=False,
        ) as mock_fn:
            result = coll.remove_item(ITEM_URN)

        mock_fn.assert_called_once_with(ivcap, COLL_URN, ITEM_URN)
        assert result is False

    def test_returns_true_when_retracted(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")

        with patch(
            "ivcap_client.collection.remove_item_from_collection",
            return_value=True,
        ) as mock_fn:
            result = coll.remove_item(ITEM_URN)

        mock_fn.assert_called_once_with(ivcap, COLL_URN, ITEM_URN)
        assert result is True


# ---------------------------------------------------------------------------
# Collection.refresh
# ---------------------------------------------------------------------------


class TestCollectionRefresh:
    def test_refresh_updates_name(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Old Name")

        list_item = _make_list_item_rt(
            content_dict={"name": "New Name", "description": "Updated"}
        )
        response = _make_ok_response(_make_aspect_list_rt(items=[list_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed", return_value=response
        ):
            returned = coll.refresh()

        assert returned is coll  # in-place update returns self
        assert coll.name == "New Name"
        assert coll.description == "Updated"


# ---------------------------------------------------------------------------
# retract_collection — logic tests
# ---------------------------------------------------------------------------

ITEM_ASPECT_URN_1 = "urn:ivcap:aspect:aaaa-0001"
ITEM_ASPECT_URN_2 = "urn:ivcap:aspect:aaaa-0002"
DEF_ASPECT_URN = "urn:ivcap:aspect:def0-0001"


def _make_item_rt(aspect_id: str) -> SimpleNamespace:
    """Build a minimal item AspectListItemRT with a given aspect id."""
    item = SimpleNamespace()
    item.id = aspect_id
    item.entity = COLL_URN
    item.schema = COLLECTION_ITEM_SCHEMA
    item.valid_from = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
    item.valid_to = UNSET
    item.additional_properties = {}
    item.content = UNSET
    return item


def _make_def_rt(aspect_id: str = DEF_ASPECT_URN) -> SimpleNamespace:
    item = SimpleNamespace()
    item.id = aspect_id
    item.entity = COLL_URN
    item.schema = COLLECTION_SCHEMA
    item.valid_from = datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC)
    item.valid_to = UNSET
    item.additional_properties = {}
    item.content = UNSET
    return item


def _retract_204():
    r = SimpleNamespace()
    r.status_code = HTTPStatus(204)
    r.parsed = None
    return r


class TestRetractCollection:
    def test_missing_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            retract_collection(_ivcap(), "")

    def test_none_urn_raises(self):
        with pytest.raises(MissingParameterValue, match="collection"):
            retract_collection(_ivcap(), None)

    def test_raises_resource_not_found_when_no_definition(self):
        """If no collection.1 aspect is found, raise ResourceNotFound."""
        ivcap = _ivcap()
        # First list call: no items (empty collection)
        # Second list call (definition): no items
        empty = _make_ok_response(_make_aspect_list_rt(items=[]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            return_value=empty,
        ):
            with pytest.raises(ResourceNotFound):
                retract_collection(ivcap, COLL_URN)

    def test_retracts_items_then_definition(self):
        """Items are retracted before the definition; total count is returned."""
        ivcap = _ivcap()
        item1 = _make_item_rt(ITEM_ASPECT_URN_1)
        item2 = _make_item_rt(ITEM_ASPECT_URN_2)
        def_item = _make_def_rt()

        # list calls: first → two items (no next page), second → definition
        items_response = _make_ok_response(_make_aspect_list_rt(items=[item1, item2]))
        def_response = _make_ok_response(_make_aspect_list_rt(items=[def_item]))
        list_responses = [items_response, def_response]

        retract_responses = [_retract_204(), _retract_204(), _retract_204()]

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            side_effect=list_responses,
        ):
            with patch(
                "ivcap_client.collection.aspect_retract.sync_detailed",
                side_effect=retract_responses,
            ) as mock_retract:
                count = retract_collection(ivcap, COLL_URN)

        assert count == 3  # 2 items + 1 definition
        # Verify retraction order: item aspects first, then definition
        calls = [c.args[0] for c in mock_retract.call_args_list]
        assert calls == [ITEM_ASPECT_URN_1, ITEM_ASPECT_URN_2, DEF_ASPECT_URN]

    def test_empty_collection_retracts_only_definition(self):
        """A collection with no items: only the definition aspect is retracted."""
        ivcap = _ivcap()
        def_item = _make_def_rt()

        empty_items = _make_ok_response(_make_aspect_list_rt(items=[]))
        def_response = _make_ok_response(_make_aspect_list_rt(items=[def_item]))
        list_responses = [empty_items, def_response]

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            side_effect=list_responses,
        ):
            with patch(
                "ivcap_client.collection.aspect_retract.sync_detailed",
                return_value=_retract_204(),
            ) as mock_retract:
                count = retract_collection(ivcap, COLL_URN)

        assert count == 1
        mock_retract.assert_called_once_with(DEF_ASPECT_URN, client=ivcap._client)

    def test_items_query_uses_correct_schema_and_entity(self):
        """The first list call must query collection-item.1 for the collection entity."""
        ivcap = _ivcap()
        empty_items = _make_ok_response(_make_aspect_list_rt(items=[]))
        def_item = _make_def_rt()
        def_response = _make_ok_response(_make_aspect_list_rt(items=[def_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            side_effect=[empty_items, def_response],
        ) as mock_list:
            with patch(
                "ivcap_client.collection.aspect_retract.sync_detailed",
                return_value=_retract_204(),
            ):
                retract_collection(ivcap, COLL_URN)

        first_call = mock_list.call_args_list[0][1]
        assert first_call["entity"] == COLL_URN
        assert first_call["schema"] == COLLECTION_ITEM_SCHEMA
        assert first_call.get("include_content") is False

    def test_definition_query_uses_correct_schema_and_entity(self):
        """The definition list call must query collection.1 for the collection entity."""
        ivcap = _ivcap()
        empty_items = _make_ok_response(_make_aspect_list_rt(items=[]))
        def_item = _make_def_rt()
        def_response = _make_ok_response(_make_aspect_list_rt(items=[def_item]))

        with patch(
            "ivcap_client.collection.aspect_list.sync_detailed",
            side_effect=[empty_items, def_response],
        ) as mock_list:
            with patch(
                "ivcap_client.collection.aspect_retract.sync_detailed",
                return_value=_retract_204(),
            ):
                retract_collection(ivcap, COLL_URN)

        second_call = mock_list.call_args_list[1][1]
        assert second_call["entity"] == COLL_URN
        assert second_call["schema"] == COLLECTION_SCHEMA


# ---------------------------------------------------------------------------
# Collection.retract — delegates to retract_collection
# ---------------------------------------------------------------------------


class TestCollectionRetract:
    def test_delegates_to_module_function(self):
        ivcap = _ivcap()
        coll = Collection(ivcap, urn=COLL_URN, name="Test")

        with patch(
            "ivcap_client.collection.retract_collection",
            return_value=5,
        ) as mock_fn:
            result = coll.retract()

        mock_fn.assert_called_once_with(ivcap, COLL_URN)
        assert result == 5
