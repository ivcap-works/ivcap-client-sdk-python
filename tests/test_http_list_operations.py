"""MockTransport-based tests for list_artifacts, list_orders, list_aspects,
and the get_service_by_name error paths.

These tests exercise the iterator + model-parsing code end-to-end without
any real network traffic.
"""

import httpx
import pytest

from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import (
    AmbiguousRequest,
    NotAuthorizedException,
    ResourceNotFound,
)
from ivcap_client.ivcap import IVCAP

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BASE_URL = "http://test"
TOKEN = "token"


def _links(path: str) -> list:
    return [{"href": f"{BASE_URL}{path}", "rel": "self", "type": "application/json"}]


def _make_iv(handler) -> IVCAP:
    iv = IVCAP(url=BASE_URL, token=TOKEN)
    iv._client = AuthenticatedClient(
        base_url=BASE_URL,
        token=TOKEN,
        httpx_args={"transport": httpx.MockTransport(handler)},
    )
    return iv


# ---------------------------------------------------------------------------
# list_artifacts
# ---------------------------------------------------------------------------


def test_list_artifacts_returns_parsed_items():
    payload = {
        "items": [
            {
                "id": "urn:ivcap:artifact:abc",
                "href": f"{BASE_URL}/1/artifacts/urn:ivcap:artifact:abc",
                "status": "ready",
                "name": "my-file.txt",
                "created-at": "2020-01-01T00:00:00Z",
            }
        ],
        "links": _links("/1/artifacts"),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/1/artifacts"
        assert request.headers.get("Authorization") == f"Bearer {TOKEN}"
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    artifacts = list(iv.list_artifacts(limit=1))
    assert len(artifacts) == 1
    assert artifacts[0].id == "urn:ivcap:artifact:abc"
    assert artifacts[0].name == "my-file.txt"


def test_list_artifacts_empty_list():
    payload = {"items": [], "links": _links("/1/artifacts")}

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    artifacts = list(iv.list_artifacts(limit=5))
    assert artifacts == []


def test_list_artifacts_401_raises_not_authorized():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "unauthorized"})

    iv = _make_iv(handler)
    with pytest.raises(NotAuthorizedException):
        list(iv.list_artifacts(limit=1))


# ---------------------------------------------------------------------------
# list_orders
# ---------------------------------------------------------------------------


def test_list_orders_returns_parsed_items():
    payload = {
        "at-time": "2020-01-01T00:00:00Z",
        "items": [
            {
                "id": "urn:ivcap:order:xyz",
                "href": f"{BASE_URL}/1/orders/urn:ivcap:order:xyz",
                "account": "urn:ivcap:account:abc",
                "service": "urn:ivcap:service:abc",
                "status": "succeeded",
            }
        ],
        "links": _links("/1/orders"),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/1/orders"
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    orders = list(iv.list_orders(limit=1))
    assert len(orders) == 1
    assert orders[0].id == "urn:ivcap:order:xyz"


def test_list_orders_401_raises_not_authorized():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "unauthorized"})

    iv = _make_iv(handler)
    with pytest.raises(NotAuthorizedException):
        list(iv.list_orders(limit=1))


# ---------------------------------------------------------------------------
# list_aspects
# ---------------------------------------------------------------------------


def test_list_aspects_returns_parsed_items():
    payload = {
        "at-time": "2020-01-01T00:00:00Z",
        "items": [
            {
                "id": "urn:ivcap:aspect:123",
                "entity": "urn:ivcap:artifact:abc",
                "schema": "urn:test:schema:1",
                "content-type": "application/json",
                "valid-from": "2020-01-01T00:00:00Z",
            }
        ],
        "links": _links("/1/aspects"),
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/1/aspects"
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    aspects = list(iv.list_aspects(limit=1))
    assert len(aspects) == 1
    assert aspects[0].id == "urn:ivcap:aspect:123"
    assert aspects[0].entity == "urn:ivcap:artifact:abc"
    assert aspects[0].schema == "urn:test:schema:1"


def test_list_aspects_401_raises_not_authorized():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "unauthorized"})

    iv = _make_iv(handler)
    with pytest.raises(NotAuthorizedException):
        list(iv.list_aspects(limit=1))


# ---------------------------------------------------------------------------
# get_service_by_name – error paths
# ---------------------------------------------------------------------------

_SVC_LIST_TEMPLATE = {
    "at-time": "2020-01-01T00:00:00Z",
    "links": [
        {"href": f"{BASE_URL}/1/services2", "rel": "self", "type": "application/json"}
    ],
}


def test_get_service_by_name_not_found_raises_resource_not_found():
    payload = {**_SVC_LIST_TEMPLATE, "items": []}

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    with pytest.raises(ResourceNotFound):
        iv.get_service_by_name("no-such-service")


def test_get_service_by_name_ambiguous_raises():
    payload = {
        **_SVC_LIST_TEMPLATE,
        "items": [
            {
                "id": "urn:ivcap:service:a",
                "name": "svc",
                "controller-schema": "urn:ivcap:schema.service.1",
                "href": f"{BASE_URL}/1/services/urn:ivcap:service:a",
            },
            {
                "id": "urn:ivcap:service:b",
                "name": "svc",
                "controller-schema": "urn:ivcap:schema.service.1",
                "href": f"{BASE_URL}/1/services/urn:ivcap:service:b",
            },
        ],
    }

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    iv = _make_iv(handler)
    with pytest.raises(AmbiguousRequest):
        iv.get_service_by_name("svc")
