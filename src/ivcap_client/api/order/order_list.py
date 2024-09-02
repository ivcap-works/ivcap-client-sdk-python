import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.order_list_rt import OrderListRT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = True,
    at_time: Union[Unset, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["page"] = page

    params["filter"] = filter_

    params["order-by"] = order_by

    params["order-desc"] = order_desc

    json_at_time: Union[Unset, str] = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat()
    params["at-time"] = json_at_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/1/orders",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OrderListRT.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = True,
    at_time: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    """list order

     list orders

    Args:
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: True. Example: True.
        at_time (Union[Unset, datetime.datetime]): Return the state of the respective resources at
            that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        at_time=at_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = True,
    at_time: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    """list order

     list orders

    Args:
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: True. Example: True.
        at_time (Union[Unset, datetime.datetime]): Return the state of the respective resources at
            that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        page=page,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        at_time=at_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = True,
    at_time: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    """list order

     list orders

    Args:
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: True. Example: True.
        at_time (Union[Unset, datetime.datetime]): Return the state of the respective resources at
            that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        page=page,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        at_time=at_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, str] = UNSET,
    filter_: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = UNSET,
    order_desc: Union[Unset, bool] = True,
    at_time: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]]:
    """list order

     list orders

    Args:
        limit (Union[Unset, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, str]): The 'orderby' query option allows clients to request
            resources in either
                                ascending order using asc or descending order using desc. If asc or desc not specified,
                                then the resources will be ordered in ascending order. The request below orders Trips
            on
                                property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, bool]): When set order result in descending order. Ascending
            order is the lt. Default: True. Example: True.
        at_time (Union[Unset, datetime.datetime]): Return the state of the respective resources at
            that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, OrderListRT]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            page=page,
            filter_=filter_,
            order_by=order_by,
            order_desc=order_desc,
            at_time=at_time,
        )
    ).parsed
