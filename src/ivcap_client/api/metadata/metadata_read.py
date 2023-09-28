from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.metadata_record_rt import MetadataRecordRT
from ...models.not_implemented_t import NotImplementedT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import Response


def _get_kwargs(
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/1/metadata/{id}".format(
            id=id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MetadataRecordRT.from_dict(response.json())

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
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    """read metadata

     Show metadata by ID

    Args:
        id (str): ID of metadata to show Example: type:scope:name.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    """read metadata

     Show metadata by ID

    Args:
        id (str): ID of metadata to show Example: type:scope:name.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    """read metadata

     Show metadata by ID

    Args:
        id (str): ID of metadata to show Example: type:scope:name.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]]:
    """read metadata

     Show metadata by ID

    Args:
        id (str): ID of metadata to show Example: type:scope:name.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidScopesT, MetadataRecordRT, NotImplementedT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
