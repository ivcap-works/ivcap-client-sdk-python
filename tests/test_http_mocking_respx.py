import pytest

respx = pytest.importorskip("respx")
import httpx


def _respx_compatible_with_installed_httpx() -> bool:
    """respx and httpx have had a few breaking changes between versions.

    If they become incompatible (route matching breaks), keep the test suite green
    by skipping these demonstration tests.
    """

    try:
        with respx.mock(assert_all_mocked=True, assert_all_called=False) as mock:
            mock.get("http://test/__respx_health").respond(200, text="ok")
            r = httpx.get("http://test/__respx_health", timeout=2)
            return r.status_code == 200
    except Exception:
        return False


if not _respx_compatible_with_installed_httpx():
    pytest.skip(
        "respx appears incompatible with the installed httpx version in this environment; "
        "MockTransport tests still provide full offline coverage.",
        allow_module_level=True,
    )

from ivcap_client.exception import IvcapApiError
from ivcap_client.ivcap import IVCAP


def test_list_services_respx_route_mocking():
    """Demonstrates respx-style mocking.

    respx intercepts httpx traffic without needing to inject a transport into the SDK.
    This is handy when you *don't* want to create a custom client/transport.
    """

    base_url = "http://test"
    iv = IVCAP(url=base_url, token="token")

    payload = {
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
            }
        ],
    }

    with respx.mock(base_url=base_url) as mock:
        # Keep this route definition simple and broad.
        route = mock.get("http://test/1/services2").respond(200, json=payload)

        services = list(iv.list_services(limit=1))

        assert route.called
        assert route.calls[0].request.url.params.get("limit") == "1"
        assert len(services) == 1
        assert services[0].id == "urn:ivcap:service:abc"


def test_search_respx_route_mocking_and_error_mapping():
    base_url = "http://test"
    iv = IVCAP(url=base_url, token="token")

    with respx.mock(base_url=base_url) as mock:
        route = mock.post("http://test/1/search").respond(500, text="boom")

        # IVCAP.search uses process_error() for >=300
        with pytest.raises(IvcapApiError):
            iv.search("q")

        assert route.called
        assert route.calls[0].request.url.params.get("limit") == "10"
