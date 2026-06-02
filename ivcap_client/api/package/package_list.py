from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.list_response_body import ListResponseBody
from ...models.not_implemented_t import NotImplementedT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    tag: str | Unset = UNSET,
    page: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["tag"] = tag

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/packages/list",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT | None:
    if response.status_code == 200:
        response_200 = ListResponseBody.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403

    if response.status_code == 422:
        response_422 = InvalidParameterT.from_dict(response.json())

        return response_422

    if response.status_code == 501:
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    tag: str | Unset = UNSET,
    page: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT]:
    """list package

     list ivcap service's docker images under account

    Args:
        tag (str | Unset): docker image tag Example: test_app:1.0.1.
        page (str | Unset): page url to list Example: http://.
        limit (int | Unset): maximum number of repository items, which can have multiple tags
            Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    tag: str | Unset = UNSET,
    page: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT | None:
    """list package

     list ivcap service's docker images under account

    Args:
        tag (str | Unset): docker image tag Example: test_app:1.0.1.
        page (str | Unset): page url to list Example: http://.
        limit (int | Unset): maximum number of repository items, which can have multiple tags
            Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT
    """

    return sync_detailed(
        client=client,
        tag=tag,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    tag: str | Unset = UNSET,
    page: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT]:
    """list package

     list ivcap service's docker images under account

    Args:
        tag (str | Unset): docker image tag Example: test_app:1.0.1.
        page (str | Unset): page url to list Example: http://.
        limit (int | Unset): maximum number of repository items, which can have multiple tags
            Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT]
    """

    kwargs = _get_kwargs(
        tag=tag,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    tag: str | Unset = UNSET,
    page: str | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT | None:
    """list package

     list ivcap service's docker images under account

    Args:
        tag (str | Unset): docker image tag Example: test_app:1.0.1.
        page (str | Unset): page url to list Example: http://.
        limit (int | Unset): maximum number of repository items, which can have multiple tags
            Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListResponseBody | NotImplementedT
    """

    return (
        await asyncio_detailed(
            client=client,
            tag=tag,
            page=page,
            limit=limit,
        )
    ).parsed
