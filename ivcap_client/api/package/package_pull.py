from http import HTTPStatus
from io import BytesIO
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.packagepull_type import PackagepullType
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    ref: str,
    type_: PackagepullType,
    offset: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["ref"] = ref

    json_type_ = type_.value
    params["type"] = json_type_

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/packages/pull",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = File(payload=BytesIO(response.json()))

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
        response_503 = File(payload=BytesIO(response.json()))

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    ref: str,
    type_: PackagepullType,
    offset: Union[Unset, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    """pull package

     pull ivcap service's docker image

    Args:
        ref (str): docker image tag or layer digest Example: test_app:1.0.1.
        type_ (PackagepullType): pull type, either be manifest, config or layer Example: layer.
        offset (Union[Unset, int]): offset of the layer chunk

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        ref=ref,
        type_=type_,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    ref: str,
    type_: PackagepullType,
    offset: Union[Unset, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    """pull package

     pull ivcap service's docker image

    Args:
        ref (str): docker image tag or layer digest Example: test_app:1.0.1.
        type_ (PackagepullType): pull type, either be manifest, config or layer Example: layer.
        offset (Union[Unset, int]): offset of the layer chunk

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]
    """

    return sync_detailed(
        client=client,
        ref=ref,
        type_=type_,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    ref: str,
    type_: PackagepullType,
    offset: Union[Unset, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    """pull package

     pull ivcap service's docker image

    Args:
        ref (str): docker image tag or layer digest Example: test_app:1.0.1.
        type_ (PackagepullType): pull type, either be manifest, config or layer Example: layer.
        offset (Union[Unset, int]): offset of the layer chunk

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        ref=ref,
        type_=type_,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    ref: str,
    type_: PackagepullType,
    offset: Union[Unset, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]]:
    """pull package

     pull ivcap service's docker image

    Args:
        ref (str): docker image tag or layer digest Example: test_app:1.0.1.
        type_ (PackagepullType): pull type, either be manifest, config or layer Example: layer.
        offset (Union[Unset, int]): offset of the layer chunk

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT]
    """

    return (
        await asyncio_detailed(
            client=client,
            ref=ref,
            type_=type_,
            offset=offset,
        )
    ).parsed
