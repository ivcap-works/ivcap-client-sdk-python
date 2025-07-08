import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.aspect_list_rt import AspectListRT
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    entity: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    content_path: Union[Unset, str] = UNSET,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    filter_: Union[Unset, str] = "",
    order_by: Union[Unset, str] = "valid_from",
    order_direction: Union[Unset, str] = "DESC",
    include_content: Union[Unset, bool] = UNSET,
    page: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["entity"] = entity

    params["schema"] = schema

    params["content-path"] = content_path

    json_at_time: Union[Unset, str] = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat()
    params["at-time"] = json_at_time

    params["limit"] = limit

    params["filter"] = filter_

    params["order-by"] = order_by

    params["order-direction"] = order_direction

    params["include-content"] = include_content

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/aspects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    if response.status_code == 200:
        response_200 = AspectListRT.from_dict(response.json())

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
    if response.status_code == 415:
        response_415 = BadRequestT.from_dict(response.json())

        return response_415
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
) -> Response[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    entity: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    content_path: Union[Unset, str] = UNSET,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    filter_: Union[Unset, str] = "",
    order_by: Union[Unset, str] = "valid_from",
    order_direction: Union[Unset, str] = "DESC",
    include_content: Union[Unset, bool] = UNSET,
    page: Union[Unset, str] = UNSET,
) -> Response[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """list aspect

     Return a list of aspect aspects.

    Args:
        entity (Union[Unset, str]): Optional entity for which to request aspects Example:
            urn:blue:image.collA#12.
        schema (Union[Unset, str]): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:schema:image%.
        content_path (Union[Unset, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, datetime.datetime]): Return aspect which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: FirstName eq
            'Scott'.
        order_by (Union[Unset, str]): Optional comma-separated list of attributes to sort the list
            by.
            * entity
            * schema
            * content
            * policy
            * account
            * created_by
            * retracted_by
            * replaces
            * valid_from
            * valid_to
             Default: 'valid_from'. Example: entity,created-at.
        order_direction (Union[Unset, str]): Set the sort direction 'ASC', 'DESC' for each order-
            by element. Default: 'DESC'. Example: desc.
        include_content (Union[Unset, bool]): When set, also include aspect content in list.
            Example: True.
        page (Union[Unset, str]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        entity=entity,
        schema=schema,
        content_path=content_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_direction=order_direction,
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
    entity: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    content_path: Union[Unset, str] = UNSET,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    filter_: Union[Unset, str] = "",
    order_by: Union[Unset, str] = "valid_from",
    order_direction: Union[Unset, str] = "DESC",
    include_content: Union[Unset, bool] = UNSET,
    page: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """list aspect

     Return a list of aspect aspects.

    Args:
        entity (Union[Unset, str]): Optional entity for which to request aspects Example:
            urn:blue:image.collA#12.
        schema (Union[Unset, str]): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:schema:image%.
        content_path (Union[Unset, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, datetime.datetime]): Return aspect which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: FirstName eq
            'Scott'.
        order_by (Union[Unset, str]): Optional comma-separated list of attributes to sort the list
            by.
            * entity
            * schema
            * content
            * policy
            * account
            * created_by
            * retracted_by
            * replaces
            * valid_from
            * valid_to
             Default: 'valid_from'. Example: entity,created-at.
        order_direction (Union[Unset, str]): Set the sort direction 'ASC', 'DESC' for each order-
            by element. Default: 'DESC'. Example: desc.
        include_content (Union[Unset, bool]): When set, also include aspect content in list.
            Example: True.
        page (Union[Unset, str]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return sync_detailed(
        client=client,
        entity=entity,
        schema=schema,
        content_path=content_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_direction=order_direction,
        include_content=include_content,
        page=page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    entity: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    content_path: Union[Unset, str] = UNSET,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    filter_: Union[Unset, str] = "",
    order_by: Union[Unset, str] = "valid_from",
    order_direction: Union[Unset, str] = "DESC",
    include_content: Union[Unset, bool] = UNSET,
    page: Union[Unset, str] = UNSET,
) -> Response[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """list aspect

     Return a list of aspect aspects.

    Args:
        entity (Union[Unset, str]): Optional entity for which to request aspects Example:
            urn:blue:image.collA#12.
        schema (Union[Unset, str]): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:schema:image%.
        content_path (Union[Unset, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, datetime.datetime]): Return aspect which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: FirstName eq
            'Scott'.
        order_by (Union[Unset, str]): Optional comma-separated list of attributes to sort the list
            by.
            * entity
            * schema
            * content
            * policy
            * account
            * created_by
            * retracted_by
            * replaces
            * valid_from
            * valid_to
             Default: 'valid_from'. Example: entity,created-at.
        order_direction (Union[Unset, str]): Set the sort direction 'ASC', 'DESC' for each order-
            by element. Default: 'DESC'. Example: desc.
        include_content (Union[Unset, bool]): When set, also include aspect content in list.
            Example: True.
        page (Union[Unset, str]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        entity=entity,
        schema=schema,
        content_path=content_path,
        at_time=at_time,
        limit=limit,
        filter_=filter_,
        order_by=order_by,
        order_direction=order_direction,
        include_content=include_content,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    entity: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    content_path: Union[Unset, str] = UNSET,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    filter_: Union[Unset, str] = "",
    order_by: Union[Unset, str] = "valid_from",
    order_direction: Union[Unset, str] = "DESC",
    include_content: Union[Unset, bool] = UNSET,
    page: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """list aspect

     Return a list of aspect aspects.

    Args:
        entity (Union[Unset, str]): Optional entity for which to request aspects Example:
            urn:blue:image.collA#12.
        schema (Union[Unset, str]): Schema prefix using '%' as wildcard indicator Example:
            urn:blue:schema:image%.
        content_path (Union[Unset, str]): To learn more about the supported format, see
                                                https://www.postgresql.org/docs/current/datatype-json.html#DATATYPE-JSONPATH Example:
            $.images[*] ? (@.size > 10000).
        at_time (Union[Unset, datetime.datetime]): Return aspect which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        filter_ (Union[Unset, str]): The 'filter' system query option allows clients to filter a
            collection of
                                        resources that are addressed by a request URL. The expression specified with 'filter'
                                        is evaluated for each resource in the collection, and only items where the expression
                                        evaluates to true are included in the response. Default: ''. Example: FirstName eq
            'Scott'.
        order_by (Union[Unset, str]): Optional comma-separated list of attributes to sort the list
            by.
            * entity
            * schema
            * content
            * policy
            * account
            * created_by
            * retracted_by
            * replaces
            * valid_from
            * valid_to
             Default: 'valid_from'. Example: entity,created-at.
        order_direction (Union[Unset, str]): Set the sort direction 'ASC', 'DESC' for each order-
            by element. Default: 'DESC'. Example: desc.
        include_content (Union[Unset, bool]): When set, also include aspect content in list.
            Example: True.
        page (Union[Unset, str]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AspectListRT, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return (
        await asyncio_detailed(
            client=client,
            entity=entity,
            schema=schema,
            content_path=content_path,
            at_time=at_time,
            limit=limit,
            filter_=filter_,
            order_by=order_by,
            order_direction=order_direction,
            include_content=include_content,
            page=page,
        )
    ).parsed
