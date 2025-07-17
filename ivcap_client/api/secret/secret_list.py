from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

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
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["page"] = page

    params["filter"] = filter_

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/1/secrets/list",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListResponseBody2.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterT.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = BadRequestT.from_dict(response.json())

        return response_501
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
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
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, None, str]): page url to list Example: https://.
        filter_ (Union[Unset, None, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, None, str]): offset token of secrets Example: 10.
        limit (Union[Unset, None, int]): maximum number of secrets Example: 10.

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
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, None, str]): page url to list Example: https://.
        filter_ (Union[Unset, None, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, None, str]): offset token of secrets Example: 10.
        limit (Union[Unset, None, int]): maximum number of secrets Example: 10.

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
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, None, str]): page url to list Example: https://.
        filter_ (Union[Unset, None, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, None, str]): offset token of secrets Example: 10.
        limit (Union[Unset, None, int]): maximum number of secrets Example: 10.

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
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ListResponseBody2]]:
    """list secret

     list secrets under account

    Args:
        page (Union[Unset, None, str]): page url to list Example: https://.
        filter_ (Union[Unset, None, str]): filter of name pattern Example: test.*.
        offset (Union[Unset, None, str]): offset token of secrets Example: 10.
        limit (Union[Unset, None, int]): maximum number of secrets Example: 10.

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
