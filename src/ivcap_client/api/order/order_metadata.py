from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.partial_meta_list_t import PartialMetaListT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    order_id: str,
    *,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["order-by"] = order_by

    params["order-desc"] = order_desc

    params["limit"] = limit

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/1/orders/{order_id}/metadata",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PartialMetaListT.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterT.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.FAILED_DEPENDENCY:
        response_424 = BadRequestT.from_dict(response.json())

        return response_424
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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
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
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
    """metadata order

     list metadata created by an order

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: False.
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        order_by=order_by,
        order_desc=order_desc,
        limit=limit,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    order_id: str,
    *,
    client: AuthenticatedClient,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
    """metadata order

     list metadata created by an order

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: False.
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]
    """

    return sync_detailed(
        order_id=order_id,
        client=client,
        order_by=order_by,
        order_desc=order_desc,
        limit=limit,
        page=page,
    ).parsed


async def asyncio_detailed(
    order_id: str,
    *,
    client: AuthenticatedClient,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
    """metadata order

     list metadata created by an order

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: False.
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        order_by=order_by,
        order_desc=order_desc,
        limit=limit,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    order_id: str,
    *,
    client: AuthenticatedClient,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]]:
    """metadata order

     list metadata created by an order

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: False.
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PartialMetaListT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
            order_by=order_by,
            order_desc=order_desc,
            limit=limit,
            page=page,
        )
    ).parsed
