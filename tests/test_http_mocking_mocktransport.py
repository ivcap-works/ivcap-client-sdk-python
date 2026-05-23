import datetime

import httpx
import pytest

from ivcap_client.client.client import AuthenticatedClient
from ivcap_client.exception import NotAuthorizedException
from ivcap_client.ivcap import IVCAP


def _service_list_payload(*, base_url: str) -> dict:
    return {
        "at-time": "2020-01-01T00:00:00Z",
        "items": [
            {
                "controller-schema": "urn:ivcap:schema.service.argo.1",
                "href": f"{base_url}/1/services/urn:ivcap:service:abc",
                "id": "urn:ivcap:service:abc",
                "name": "svc",
                "description": "a service",
            }
        ],
        "links": [
            {
                "href": f"{base_url}/1/services2",
                "rel": "self",
                "type": "application/json",
            },
        ],
    }


def _search_payload(*, base_url: str) -> dict:
    return {
        "at-time": "2020-01-01T00:00:00Z",
        "items": ["result-1", "result-2"],
        "links": [
            {"href": f"{base_url}/1/search", "rel": "self", "type": "application/json"},
        ],
    }


def test_list_services_mocktransport_injected_via_httpx_args():
    """Demonstrates the recommended *no extra dependency* approach.

    We inject an httpx transport via AuthenticatedClient(httpx_args={"transport": ...}).
    This keeps the OpenAPI-generated layer untouched and still exercises the real
    request building/parsing code.
    """

    base_url = "http://test"
    seen_requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_requests.append(request)

        assert request.method == "GET"
        assert request.url.path == "/1/services2"
        # BaseIter passes the requested limit through
        assert request.url.params.get("limit") == "2"
        assert request.headers.get("Authorization") == "Bearer token"

        return httpx.Response(200, json=_service_list_payload(base_url=base_url))

    transport = httpx.MockTransport(handler)
    iv = IVCAP(url=base_url, token="token")
    iv._client = AuthenticatedClient(
        base_url=base_url, token="token", httpx_args={"transport": transport}
    )

    services = list(iv.list_services(limit=2))

    assert len(seen_requests) == 1
    assert len(services) == 1
    assert services[0].id == "urn:ivcap:service:abc"
    assert services[0].name == "svc"


def test_search_mocktransport_parses_and_returns_generated_model():
    base_url = "http://test"
    query = "some datalog"
    seen_requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_requests.append(request)

        assert request.method == "POST"
        assert request.url.path == "/1/search"
        assert request.headers.get("Authorization") == "Bearer token"
        assert request.headers.get("Content-Type") == "application/datalog+mangle"

        # search_search sends the query as raw request content
        assert request.content == query.encode()

        return httpx.Response(200, json=_search_payload(base_url=base_url))

    transport = httpx.MockTransport(handler)
    iv = IVCAP(url=base_url, token="token")
    iv._client = AuthenticatedClient(
        base_url=base_url, token="token", httpx_args={"transport": transport}
    )

    result = iv.search(query)

    assert len(seen_requests) == 1
    assert result.items == ["result-1", "result-2"]
    # parsed model converts at-time to datetime
    assert isinstance(result.at_time, datetime.datetime)


def test_search_mocktransport_raises_on_403():
    base_url = "http://test"

    def handler(_: httpx.Request) -> httpx.Response:
        # Must match the OpenAPI error body shape so the generated parser
        # doesn't explode before the SDK can raise a higher-level exception.
        return httpx.Response(403, json={"message": "forbidden"})

    transport = httpx.MockTransport(handler)
    iv = IVCAP(url=base_url, token="token")
    iv._client = AuthenticatedClient(
        base_url=base_url, token="token", httpx_args={"transport": transport}
    )

    with pytest.raises(NotAuthorizedException):
        iv.search("q")
