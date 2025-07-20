from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.list_response_body_2 import ListResponseBody2
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    offset: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["filter"] = filter_

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/secrets/list",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    if response.status_code == 200:
        response_200 = ListResponseBody2.from_dict(response.json())

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
        response_501 = BadRequestT.from_dict(response.json())

        return response_501
    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    offset: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, str]): page url to list Example: https://.
        filter_ (Union[Unset, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, str]): offset token of secrets Example: 10.
        limit (Union[Unset, int]): maximum number of secrets Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]
    """

    kwargs = _get_kwargs(
        page=page,
        filter_=filter_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    offset: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, str]): page url to list Example: https://.
        filter_ (Union[Unset, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, str]): offset token of secrets Example: 10.
        limit (Union[Unset, int]): maximum number of secrets Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]
    """

    return sync_detailed(
        client=client,
        page=page,
        filter_=filter_,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    offset: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, str]): page url to list Example: https://.
        filter_ (Union[Unset, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, str]): offset token of secrets Example: 10.
        limit (Union[Unset, int]): maximum number of secrets Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]
    """

    kwargs = _get_kwargs(
        page=page,
        filter_=filter_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    offset: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, str]): page url to list Example: https://.
        filter_ (Union[Unset, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, str]): offset token of secrets Example: 10.
        limit (Union[Unset, int]): maximum number of secrets Example: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            filter_=filter_,
            offset=offset,
            limit=limit,
        )
    ).parsed
