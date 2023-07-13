import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.list_meta_rt import ListMetaRT
from ...models.not_implemented_t import NotImplementedT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    entity_id: Union[Unset, None, str] = UNSET,
    schema: Union[Unset, None, str] = UNSET,
    aspect_path: Union[Unset, None, str] = UNSET,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, int] = 10,
    filter_: Union[Unset, None, str] = "",
    order_by: Union[Unset, None, str] = "",
    order_desc: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/1/metadata".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["entity-id"] = entity_id

    params["schema"] = schema

    params["aspect-path"] = aspect_path

    json_at_time: Union[Unset, None, str] = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat() if at_time else None

    params["at-time"] = json_at_time

    params["limit"] = limit

    params["filter"] = filter_

    params["order-by"] = order_by

    params["order-desc"] = order_desc

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListMetaRT.from_dict(response.json())

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
    *, client: Client, response: httpx.Response
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    entity_id: Union[Unset, None, str] = UNSET,
    schema: Union[Unset, None, str] = UNSET,
    aspect_path: Union[Unset, None, str] = UNSET,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, int] = 10,
    filter_: Union[Unset, None, str] = "",
    order_by: Union[Unset, None, str] = "",
    order_desc: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (Union[Unset, None, str]): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (Union[Unset, None, str]): Optional schema to filter on Example: urn:blue:image%.
        aspect_path (Union[Unset, None, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, None, datetime.datetime]): Return metadata which where valid at that
            time [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: filter=FirstName
            eq 'Scott'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        page (Union[Unset, None, str]): The content of '$page' is returned in the 'links' part of
            a previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        client=client,
        entity_id=entity_id,
        schema=schema,
        aspect_path=aspect_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        page=page,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    entity_id: Union[Unset, None, str] = UNSET,
    schema: Union[Unset, None, str] = UNSET,
    aspect_path: Union[Unset, None, str] = UNSET,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, int] = 10,
    filter_: Union[Unset, None, str] = "",
    order_by: Union[Unset, None, str] = "",
    order_desc: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (Union[Unset, None, str]): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (Union[Unset, None, str]): Optional schema to filter on Example: urn:blue:image%.
        aspect_path (Union[Unset, None, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, None, datetime.datetime]): Return metadata which where valid at that
            time [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: filter=FirstName
            eq 'Scott'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        page (Union[Unset, None, str]): The content of '$page' is returned in the 'links' part of
            a previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]
    """

    return sync_detailed(
        client=client,
        entity_id=entity_id,
        schema=schema,
        aspect_path=aspect_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    entity_id: Union[Unset, None, str] = UNSET,
    schema: Union[Unset, None, str] = UNSET,
    aspect_path: Union[Unset, None, str] = UNSET,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, int] = 10,
    filter_: Union[Unset, None, str] = "",
    order_by: Union[Unset, None, str] = "",
    order_desc: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (Union[Unset, None, str]): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (Union[Unset, None, str]): Optional schema to filter on Example: urn:blue:image%.
        aspect_path (Union[Unset, None, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, None, datetime.datetime]): Return metadata which where valid at that
            time [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: filter=FirstName
            eq 'Scott'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        page (Union[Unset, None, str]): The content of '$page' is returned in the 'links' part of
            a previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        client=client,
        entity_id=entity_id,
        schema=schema,
        aspect_path=aspect_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        page=page,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    entity_id: Union[Unset, None, str] = UNSET,
    schema: Union[Unset, None, str] = UNSET,
    aspect_path: Union[Unset, None, str] = UNSET,
    at_time: Union[Unset, None, datetime.datetime] = UNSET,
    limit: Union[Unset, None, int] = 10,
    filter_: Union[Unset, None, str] = "",
    order_by: Union[Unset, None, str] = "",
    order_desc: Union[Unset, None, bool] = UNSET,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (Union[Unset, None, str]): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (Union[Unset, None, str]): Optional schema to filter on Example: urn:blue:image%.
        aspect_path (Union[Unset, None, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, None, datetime.datetime]): Return metadata which where valid at that
            time [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, None, int]): The $limit system query option requests the number of
            items in the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, None, str]): The 'filter' system query option allows clients to
            filter a collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: filter=FirstName
            eq 'Scott'.
        order_by (Union[Unset, None, str]): The 'orderby' query option allows clients to request
            resources in either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: orderby=EndsAt.
        order_desc (Union[Unset, None, bool]): When set order result in descending order.
            Ascending order is the default.
        page (Union[Unset, None, str]): The content of '$page' is returned in the 'links' part of
            a previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, ListMetaRT, NotImplementedT]
    """

    return (
        await asyncio_detailed(
            client=client,
            entity_id=entity_id,
            schema=schema,
            aspect_path=aspect_path,
            at_time=at_time,
            limit=limit,
            filter_=filter_,
            order_by=order_by,
            order_desc=order_desc,
            page=page,
        )
    ).parsed
