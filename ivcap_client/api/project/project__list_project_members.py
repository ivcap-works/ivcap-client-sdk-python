from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.members_list import MembersList
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    urn: str,
    *,
    role: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["role"] = role

    params["limit"] = limit

    params["page"] = page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/1/project/{urn}/members".format(
            urn=urn,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MembersList.from_dict(response.json())

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
        response_503 = cast(Any, None)
        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    urn: str,
    *,
    client: AuthenticatedClient,
    role: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    """List Project Members

     Lists the current members of a project.

    Args:
        urn (str): Project URN Example: urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f.
        role (Union[Unset, None, str]): Role Example: all.
        limit (Union[Unset, None, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): A pagination token to retrieve the next set of results.
            Empty if there are no more results Example: Harum minima perspiciatis delectus nihil..

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        urn=urn,
        role=role,
        limit=limit,
        page=page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    urn: str,
    *,
    client: AuthenticatedClient,
    role: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    """List Project Members

     Lists the current members of a project.

    Args:
        urn (str): Project URN Example: urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f.
        role (Union[Unset, None, str]): Role Example: all.
        limit (Union[Unset, None, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): A pagination token to retrieve the next set of results.
            Empty if there are no more results Example: Harum minima perspiciatis delectus nihil..

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]
    """

    return sync_detailed(
        urn=urn,
        client=client,
        role=role,
        limit=limit,
        page=page,
    ).parsed


async def asyncio_detailed(
    urn: str,
    *,
    client: AuthenticatedClient,
    role: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    """List Project Members

     Lists the current members of a project.

    Args:
        urn (str): Project URN Example: urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f.
        role (Union[Unset, None, str]): Role Example: all.
        limit (Union[Unset, None, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): A pagination token to retrieve the next set of results.
            Empty if there are no more results Example: Harum minima perspiciatis delectus nihil..

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        urn=urn,
        role=role,
        limit=limit,
        page=page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    urn: str,
    *,
    client: AuthenticatedClient,
    role: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = 10,
    page: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]]:
    """List Project Members

     Lists the current members of a project.

    Args:
        urn (str): Project URN Example: urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f.
        role (Union[Unset, None, str]): Role Example: all.
        limit (Union[Unset, None, int]): The 'limit' query option sets the maximum number of items
                                to be included in the result. Default: 10. Example: 10.
        page (Union[Unset, None, str]): A pagination token to retrieve the next set of results.
            Empty if there are no more results Example: Harum minima perspiciatis delectus nihil..

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, MembersList, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            urn=urn,
            client=client,
            role=role,
            limit=limit,
            page=page,
        )
    ).parsed
