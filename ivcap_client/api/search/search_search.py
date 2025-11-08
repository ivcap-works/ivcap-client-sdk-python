import datetime
from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.search_list_rt import SearchListRT
from ...models.unsupported_content_type_t import UnsupportedContentTypeT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    body: File,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, Any] = UNSET,
    content_type: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Content-Type"] = content_type

    params: dict[str, Any] = {}

    json_at_time: Union[Unset, str] = UNSET
    if not isinstance(at_time, Unset):
        json_at_time = at_time.isoformat()
    params["at-time"] = json_at_time

    params["limit"] = limit

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/search",
        "params": params,
    }

    _body = body.payload

    _kwargs["content"] = _body
    headers["Content-Type"] = "application/datalog+mangle"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    if response.status_code == 200:
        response_200 = SearchListRT.from_dict(response.json())

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
        response_415 = UnsupportedContentTypeT.from_dict(response.json())

        return response_415
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
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: File,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, Any] = UNSET,
    content_type: str,
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    """search search

     Execute query provided in body and return a list of search result.

    Args:
        at_time (Union[Unset, datetime.datetime]): Return search which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, Any]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/datalog+mangle.
        body (File): Query Example:
            # Find all the artifacts in the input collection for a specific order
            #

            # order_parameter(orderID, parameterName, parameterValue)
            :load_aspect(/order_parameter, "urn:ivcap:schema:order-placed.1", ["entity",
            ".parameters[*].name|value"]).
            # collection(collectionID, artifactID)
            :load_aspect(/collection, "urn:ivcap:schema:artifact-collection.1", [".collection",
            ".artifacts[*]"]).

            query(Artifact) :-
              # The collection ID is the 'image' parameter of the order
              order_parameter("urn:ivcap:order:550e8400-e29b-41d4-a716-446655440000", "images",
            Collection),
              collection(Collection, Artifact).
                                        .

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]]
    """

    kwargs = _get_kwargs(
        body=body,
        at_time=at_time,
        limit=limit,
        page=page,
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: File,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, Any] = UNSET,
    content_type: str,
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    """search search

     Execute query provided in body and return a list of search result.

    Args:
        at_time (Union[Unset, datetime.datetime]): Return search which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, Any]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/datalog+mangle.
        body (File): Query Example:
            # Find all the artifacts in the input collection for a specific order
            #

            # order_parameter(orderID, parameterName, parameterValue)
            :load_aspect(/order_parameter, "urn:ivcap:schema:order-placed.1", ["entity",
            ".parameters[*].name|value"]).
            # collection(collectionID, artifactID)
            :load_aspect(/collection, "urn:ivcap:schema:artifact-collection.1", [".collection",
            ".artifacts[*]"]).

            query(Artifact) :-
              # The collection ID is the 'image' parameter of the order
              order_parameter("urn:ivcap:order:550e8400-e29b-41d4-a716-446655440000", "images",
            Collection),
              collection(Collection, Artifact).
                                        .

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
    """

    return sync_detailed(
        client=client,
        body=body,
        at_time=at_time,
        limit=limit,
        page=page,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: File,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, Any] = UNSET,
    content_type: str,
) -> Response[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    """search search

     Execute query provided in body and return a list of search result.

    Args:
        at_time (Union[Unset, datetime.datetime]): Return search which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, Any]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/datalog+mangle.
        body (File): Query Example:
            # Find all the artifacts in the input collection for a specific order
            #

            # order_parameter(orderID, parameterName, parameterValue)
            :load_aspect(/order_parameter, "urn:ivcap:schema:order-placed.1", ["entity",
            ".parameters[*].name|value"]).
            # collection(collectionID, artifactID)
            :load_aspect(/collection, "urn:ivcap:schema:artifact-collection.1", [".collection",
            ".artifacts[*]"]).

            query(Artifact) :-
              # The collection ID is the 'image' parameter of the order
              order_parameter("urn:ivcap:order:550e8400-e29b-41d4-a716-446655440000", "images",
            Collection),
              collection(Collection, Artifact).
                                        .

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]]
    """

    kwargs = _get_kwargs(
        body=body,
        at_time=at_time,
        limit=limit,
        page=page,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: File,
    at_time: Union[Unset, datetime.datetime] = UNSET,
    limit: Union[Unset, int] = 10,
    page: Union[Unset, Any] = UNSET,
    content_type: str,
) -> Optional[
    Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
]:
    """search search

     Execute query provided in body and return a list of search result.

    Args:
        at_time (Union[Unset, datetime.datetime]): Return search which where valid at that time
            [now] Example: 1996-12-19T16:39:57-08:00.
        limit (Union[Unset, int]): The 'limit' system query option requests the number of items in
            the queried
                                        collection to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, Any]): The content of '$page' is returned in the 'links' part of a
            previous query and
                                        will when set, ALL other parameters, except for 'limit' are ignored. Example:
            gdsgQwhdgd.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/datalog+mangle.
        body (File): Query Example:
            # Find all the artifacts in the input collection for a specific order
            #

            # order_parameter(orderID, parameterName, parameterValue)
            :load_aspect(/order_parameter, "urn:ivcap:schema:order-placed.1", ["entity",
            ".parameters[*].name|value"]).
            # collection(collectionID, artifactID)
            :load_aspect(/collection, "urn:ivcap:schema:artifact-collection.1", [".collection",
            ".artifacts[*]"]).

            query(Artifact) :-
              # The collection ID is the 'image' parameter of the order
              order_parameter("urn:ivcap:order:550e8400-e29b-41d4-a716-446655440000", "images",
            Collection),
              collection(Collection, Artifact).
                                        .

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, NotImplementedT, SearchListRT, UnsupportedContentTypeT]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            at_time=at_time,
            limit=limit,
            page=page,
            content_type=content_type,
        )
    ).parsed
