from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.order_top_result_item import OrderTopResultItem
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import Response


def _get_kwargs(
    order_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/1/orders/{order_id}/top",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_order_top_result_item_collection_item_data in _response_200:
            componentsschemas_order_top_result_item_collection_item = OrderTopResultItem.from_dict(
                componentsschemas_order_top_result_item_collection_item_data
            )

            response_200.append(componentsschemas_order_top_result_item_collection_item)

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
    if response.status_code == 404:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
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
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    order_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    """top order

     top order resources

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list['OrderTopResultItem']]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    order_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    """top order

     top order resources

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list['OrderTopResultItem']]
    """

    return sync_detailed(
        order_id=order_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    order_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    """top order

     top order resources

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list['OrderTopResultItem']]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    order_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list["OrderTopResultItem"]]
]:
    """top order

     top order resources

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, list['OrderTopResultItem']]
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
        )
    ).parsed
