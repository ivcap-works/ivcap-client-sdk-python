from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    order_id: str,
    *,
    from_: Union[Unset, None, int] = UNSET,
    to: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["from"] = from_

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/1/orders/{orderID}/logs".format(
            orderID=order_id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = File(payload=BytesIO(response.json()))

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = BadRequestT.from_dict(response.json())

        return response_501
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = File(payload=BytesIO(response.json()))

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
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
    from_: Union[Unset, None, int] = UNSET,
    to: Union[Unset, None, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """logs order

     download order logs

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        from_ (Union[Unset, None, int]): From unix time, seconds since 1970-01-01 Example:
            1257894000.
        to (Union[Unset, None, int]): To unix time, seconds since 1970-01-01 Example: 1257894000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    order_id: str,
    *,
    client: AuthenticatedClient,
    from_: Union[Unset, None, int] = UNSET,
    to: Union[Unset, None, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """logs order

     download order logs

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        from_ (Union[Unset, None, int]): From unix time, seconds since 1970-01-01 Example:
            1257894000.
        to (Union[Unset, None, int]): To unix time, seconds since 1970-01-01 Example: 1257894000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return sync_detailed(
        order_id=order_id,
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    order_id: str,
    *,
    client: AuthenticatedClient,
    from_: Union[Unset, None, int] = UNSET,
    to: Union[Unset, None, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """logs order

     download order logs

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        from_ (Union[Unset, None, int]): From unix time, seconds since 1970-01-01 Example:
            1257894000.
        to (Union[Unset, None, int]): To unix time, seconds since 1970-01-01 Example: 1257894000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        order_id=order_id,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    order_id: str,
    *,
    client: AuthenticatedClient,
    from_: Union[Unset, None, int] = UNSET,
    to: Union[Unset, None, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """logs order

     download order logs

    Args:
        order_id (str): Reference to order requested Example:
            urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        from_ (Union[Unset, None, int]): From unix time, seconds since 1970-01-01 Example:
            1257894000.
        to (Union[Unset, None, int]): To unix time, seconds since 1970-01-01 Example: 1257894000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            order_id=order_id,
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed
