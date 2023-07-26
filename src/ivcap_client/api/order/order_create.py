from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.order_request_t import OrderRequestT
from ...models.order_status_rt import OrderStatusRT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import Response


def _get_kwargs(
    *,
    json_body: OrderRequestT,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/1/orders",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OrderStatusRT.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
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
        response_422 = InvalidParameterValue.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = NotImplementedT.from_dict(response.json())

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
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OrderRequestT,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    """create order

     Create a new orders and return its status.

    Args:
        json_body (OrderRequestT):  Example: {'accountID':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value':
            10}], 'policyID': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'serviceID':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: OrderRequestT,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    """create order

     Create a new orders and return its status.

    Args:
        json_body (OrderRequestT):  Example: {'accountID':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value':
            10}], 'policyID': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'serviceID':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: OrderRequestT,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    """create order

     Create a new orders and return its status.

    Args:
        json_body (OrderRequestT):  Example: {'accountID':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value':
            10}], 'policyID': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'serviceID':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: OrderRequestT,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]]:
    """create order

     Create a new orders and return its status.

    Args:
        json_body (OrderRequestT):  Example: {'accountID':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value':
            10}], 'policyID': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'serviceID':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderStatusRT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
