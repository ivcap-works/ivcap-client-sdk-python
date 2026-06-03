import datetime
from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.list_meta_rt import ListMetaRT
from ...models.not_implemented_t import NotImplementedT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    entity_id: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    aspect_path: str | Unset = UNSET,
    at_time: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 10,
    filter_: str | Unset = "",
    order_by: str | Unset = "",
    order_desc: bool | Unset = UNSET,
    include_content: bool | Unset = True,
    page: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["entity-id"] = entity_id

    params["schema"] = schema

    params["aspect-path"] = aspect_path

    json_at_time: str | Unset = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat()
    params["at-time"] = json_at_time

    params["limit"] = limit

    params["filter"] = filter_

    params["order-by"] = order_by

    params["order-desc"] = order_desc

    params["include-content"] = include_content

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/metadata",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT | None:
    if response.status_code == 200:
        response_200 = ListMetaRT.from_dict(response.json())

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
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    entity_id: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    aspect_path: str | Unset = UNSET,
    at_time: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 10,
    filter_: str | Unset = "",
    order_by: str | Unset = "",
    order_desc: bool | Unset = UNSET,
    include_content: bool | Unset = True,
    page: str | Unset = UNSET,
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (str | Unset): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (str | Unset): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:image%.
        aspect_path (str | Unset): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (datetime.datetime | Unset): Return metadata which where valid at that time [now]
            Example: 1996-12-19T16:39:57-08:00.
        limit (int | Unset): The 'limit' system query option requests the number of items in the
            queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (str | Unset): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: name~='Scott'.
        order_by (str | Unset): The 'orderby' query option allows clients to request resources in
            either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: name.
        order_desc (bool | Unset): When set order result in descending order. Ascending order is
            the default. Example: True.
        include_content (bool | Unset): When set, also include aspect content in list. Default:
            True. Example: True.
        page (str | Unset): The content of '$page' is returned in the 'links' part of a previous
            query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
        schema=schema,
        aspect_path=aspect_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        include_content=include_content,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    entity_id: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    aspect_path: str | Unset = UNSET,
    at_time: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 10,
    filter_: str | Unset = "",
    order_by: str | Unset = "",
    order_desc: bool | Unset = UNSET,
    include_content: bool | Unset = True,
    page: str | Unset = UNSET,
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT | None:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (str | Unset): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (str | Unset): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:image%.
        aspect_path (str | Unset): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (datetime.datetime | Unset): Return metadata which where valid at that time [now]
            Example: 1996-12-19T16:39:57-08:00.
        limit (int | Unset): The 'limit' system query option requests the number of items in the
            queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (str | Unset): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: name~='Scott'.
        order_by (str | Unset): The 'orderby' query option allows clients to request resources in
            either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: name.
        order_desc (bool | Unset): When set order result in descending order. Ascending order is
            the default. Example: True.
        include_content (bool | Unset): When set, also include aspect content in list. Default:
            True. Example: True.
        page (str | Unset): The content of '$page' is returned in the 'links' part of a previous
            query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT
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
        include_content=include_content,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    entity_id: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    aspect_path: str | Unset = UNSET,
    at_time: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 10,
    filter_: str | Unset = "",
    order_by: str | Unset = "",
    order_desc: bool | Unset = UNSET,
    include_content: bool | Unset = True,
    page: str | Unset = UNSET,
) -> Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT]:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (str | Unset): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (str | Unset): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:image%.
        aspect_path (str | Unset): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (datetime.datetime | Unset): Return metadata which where valid at that time [now]
            Example: 1996-12-19T16:39:57-08:00.
        limit (int | Unset): The 'limit' system query option requests the number of items in the
            queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (str | Unset): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: name~='Scott'.
        order_by (str | Unset): The 'orderby' query option allows clients to request resources in
            either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: name.
        order_desc (bool | Unset): When set order result in descending order. Ascending order is
            the default. Example: True.
        include_content (bool | Unset): When set, also include aspect content in list. Default:
            True. Example: True.
        page (str | Unset): The content of '$page' is returned in the 'links' part of a previous
            query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT]
    """

    kwargs = _get_kwargs(
        entity_id=entity_id,
        schema=schema,
        aspect_path=aspect_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_desc=order_desc,
        include_content=include_content,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    entity_id: str | Unset = UNSET,
    schema: str | Unset = UNSET,
    aspect_path: str | Unset = UNSET,
    at_time: datetime.datetime | Unset = UNSET,
    limit: int | Unset = 10,
    filter_: str | Unset = "",
    order_by: str | Unset = "",
    order_desc: bool | Unset = UNSET,
    include_content: bool | Unset = True,
    page: str | Unset = UNSET,
) -> Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT | None:
    """list metadata

     Return a list of metadata records.

    Args:
        entity_id (str | Unset): Entity for which to request metadata Example:
            urn:blue:image.collA.12.
        schema (str | Unset): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:image%.
        aspect_path (str | Unset): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (datetime.datetime | Unset): Return metadata which where valid at that time [now]
            Example: 1996-12-19T16:39:57-08:00.
        limit (int | Unset): The 'limit' system query option requests the number of items in the
            queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (str | Unset): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: name~='Scott'.
        order_by (str | Unset): The 'orderby' query option allows clients to request resources in
            either
                                        ascending order using asc or descending order using desc. If asc or desc not
            specified,
                                        then the resources will be ordered in ascending order. The request below orders Trips
            on
                                        property EndsAt in descending order. Default: ''. Example: name.
        order_desc (bool | Unset): When set order result in descending order. Ascending order is
            the default. Example: True.
        include_content (bool | Unset): When set, also include aspect content in list. Default:
            True. Example: True.
        page (str | Unset): The content of '$page' is returned in the 'links' part of a previous
            query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | ListMetaRT | NotImplementedT
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
            include_content=include_content,
            page=page,
        )
    ).parsed
