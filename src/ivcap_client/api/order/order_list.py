import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.order_list_rt import OrderListRT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    order_desc: Union[Unset, None, bool] = False,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["page"] = page

    params["filter"] = filter_

    params["order-by"] = order_by

    params["order-desc"] = order_desc

    json_at_time: Union[Unset, None, str] = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat() if at_time else None

    params["at-time"] = json_at_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/1/orders",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OrderListRT.from_dict(response.json())

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
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterValue.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    order_desc: Union[Unset, None, bool] = False,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    """list order

     orders

    Args:
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        at_time (Union[Unset, None, datetime.datetime]): Return the state of the respective
            resources at that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]
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
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    order_desc: Union[Unset, None, bool] = False,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    """list order

     orders

    Args:
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        at_time (Union[Unset, None, datetime.datetime]): Return the state of the respective
            resources at that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]
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
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    order_desc: Union[Unset, None, bool] = False,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    """list order

     orders

    Args:
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        at_time (Union[Unset, None, datetime.datetime]): Return the state of the respective
            resources at that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]
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
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
    order_by: Union[Unset, None, str] = UNSET,
    order_desc: Union[Unset, None, bool] = False,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]]:
    """list order

     orders

    Args:
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): The content of 'page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Example: name ~= 'Scott%'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        at_time (Union[Unset, None, datetime.datetime]): Return the state of the respective
            resources at that time [now] Example: 1996-12-19T16:39:57-08:00.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, OrderListRT]
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
