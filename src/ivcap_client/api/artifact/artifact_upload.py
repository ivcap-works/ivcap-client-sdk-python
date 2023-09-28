from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.artifact_status_rt import ArtifactStatusRT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    content_type: Union[Unset, str] = UNSET,
    content_encoding: Union[Unset, str] = UNSET,
    content_length: Union[Unset, int] = UNSET,
    x_name: Union[Unset, str] = UNSET,
    x_collection: Union[Unset, str] = UNSET,
    x_content_type: Union[Unset, str] = UNSET,
    x_content_length: Union[Unset, int] = UNSET,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers = {}
    if not isinstance(content_type, Unset):
        headers["Content-Type"] = content_type

    if not isinstance(content_encoding, Unset):
        headers["Content-Encoding"] = content_encoding

    if not isinstance(content_length, Unset):
        headers["Content-Length"] = str(content_length)

    if not isinstance(x_name, Unset):
        headers["X-Name"] = x_name

    if not isinstance(x_collection, Unset):
        headers["X-Collection"] = x_collection

    if not isinstance(x_content_type, Unset):
        headers["X-Content-Type"] = x_content_type

    if not isinstance(x_content_length, Unset):
        headers["X-Content-Length"] = str(x_content_length)

    if not isinstance(upload_length, Unset):
        headers["Upload-Length"] = str(upload_length)

    if not isinstance(tus_resumable, Unset):
        headers["Tus-Resumable"] = tus_resumable

    return {
        "method": "post",
        "url": "/1/artifacts",
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ArtifactStatusRT.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    content_type: Union[Unset, str] = UNSET,
    content_encoding: Union[Unset, str] = UNSET,
    content_length: Union[Unset, int] = UNSET,
    x_name: Union[Unset, str] = UNSET,
    x_collection: Union[Unset, str] = UNSET,
    x_content_type: Union[Unset, str] = UNSET,
    x_content_length: Union[Unset, int] = UNSET,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    """upload artifact

     Upload content and create a artifacts.

    Args:
        content_type (Union[Unset, str]): Content-Type header, MUST define type of uploaded
            content. Example: application/x-netcdf4.
        content_encoding (Union[Unset, str]): Content-Encoding header, MAY define encoding of
            content. Example: gzip.
        content_length (Union[Unset, int]): Content-Length header, MAY define size of expected
            upload. Example: 2376.
        x_name (Union[Unset, str]): X-Name header, MAY define a more human friendly name. Reusing
            a name will NOT override an existing artifact with the same name Example: field-trip-
            jun-22.
        x_collection (Union[Unset, str]): X-Collection header, MAY define an collection name as a
            simple way of grouping artifacts Example: field-trip-jun-22.
        x_content_type (Union[Unset, str]): X-Content-Type header, used for initial, empty content
            creation requests. Example: application/x-netcdf4.
        x_content_length (Union[Unset, int]): X-Content-Length header, used for initial, empty
            content creation requests. Example: 2376.
        upload_length (Union[Unset, int]): Upload-Length header, sets the expected content size
            part of the TUS protocol. Example: 2376.
        tus_resumable (Union[Unset, str]): Tus-Resumable header, specifies TUS protocol version.
            Example: 1.0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
        content_encoding=content_encoding,
        content_length=content_length,
        x_name=x_name,
        x_collection=x_collection,
        x_content_type=x_content_type,
        x_content_length=x_content_length,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    content_type: Union[Unset, str] = UNSET,
    content_encoding: Union[Unset, str] = UNSET,
    content_length: Union[Unset, int] = UNSET,
    x_name: Union[Unset, str] = UNSET,
    x_collection: Union[Unset, str] = UNSET,
    x_content_type: Union[Unset, str] = UNSET,
    x_content_length: Union[Unset, int] = UNSET,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    """upload artifact

     Upload content and create a artifacts.

    Args:
        content_type (Union[Unset, str]): Content-Type header, MUST define type of uploaded
            content. Example: application/x-netcdf4.
        content_encoding (Union[Unset, str]): Content-Encoding header, MAY define encoding of
            content. Example: gzip.
        content_length (Union[Unset, int]): Content-Length header, MAY define size of expected
            upload. Example: 2376.
        x_name (Union[Unset, str]): X-Name header, MAY define a more human friendly name. Reusing
            a name will NOT override an existing artifact with the same name Example: field-trip-
            jun-22.
        x_collection (Union[Unset, str]): X-Collection header, MAY define an collection name as a
            simple way of grouping artifacts Example: field-trip-jun-22.
        x_content_type (Union[Unset, str]): X-Content-Type header, used for initial, empty content
            creation requests. Example: application/x-netcdf4.
        x_content_length (Union[Unset, int]): X-Content-Length header, used for initial, empty
            content creation requests. Example: 2376.
        upload_length (Union[Unset, int]): Upload-Length header, sets the expected content size
            part of the TUS protocol. Example: 2376.
        tus_resumable (Union[Unset, str]): Tus-Resumable header, specifies TUS protocol version.
            Example: 1.0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]
    """

    return sync_detailed(
        client=client,
        content_type=content_type,
        content_encoding=content_encoding,
        content_length=content_length,
        x_name=x_name,
        x_collection=x_collection,
        x_content_type=x_content_type,
        x_content_length=x_content_length,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    content_type: Union[Unset, str] = UNSET,
    content_encoding: Union[Unset, str] = UNSET,
    content_length: Union[Unset, int] = UNSET,
    x_name: Union[Unset, str] = UNSET,
    x_collection: Union[Unset, str] = UNSET,
    x_content_type: Union[Unset, str] = UNSET,
    x_content_length: Union[Unset, int] = UNSET,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: Union[Unset, str] = UNSET,
) -> Response[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    """upload artifact

     Upload content and create a artifacts.

    Args:
        content_type (Union[Unset, str]): Content-Type header, MUST define type of uploaded
            content. Example: application/x-netcdf4.
        content_encoding (Union[Unset, str]): Content-Encoding header, MAY define encoding of
            content. Example: gzip.
        content_length (Union[Unset, int]): Content-Length header, MAY define size of expected
            upload. Example: 2376.
        x_name (Union[Unset, str]): X-Name header, MAY define a more human friendly name. Reusing
            a name will NOT override an existing artifact with the same name Example: field-trip-
            jun-22.
        x_collection (Union[Unset, str]): X-Collection header, MAY define an collection name as a
            simple way of grouping artifacts Example: field-trip-jun-22.
        x_content_type (Union[Unset, str]): X-Content-Type header, used for initial, empty content
            creation requests. Example: application/x-netcdf4.
        x_content_length (Union[Unset, int]): X-Content-Length header, used for initial, empty
            content creation requests. Example: 2376.
        upload_length (Union[Unset, int]): Upload-Length header, sets the expected content size
            part of the TUS protocol. Example: 2376.
        tus_resumable (Union[Unset, str]): Tus-Resumable header, specifies TUS protocol version.
            Example: 1.0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
        content_encoding=content_encoding,
        content_length=content_length,
        x_name=x_name,
        x_collection=x_collection,
        x_content_type=x_content_type,
        x_content_length=x_content_length,
        upload_length=upload_length,
        tus_resumable=tus_resumable,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    content_type: Union[Unset, str] = UNSET,
    content_encoding: Union[Unset, str] = UNSET,
    content_length: Union[Unset, int] = UNSET,
    x_name: Union[Unset, str] = UNSET,
    x_collection: Union[Unset, str] = UNSET,
    x_content_type: Union[Unset, str] = UNSET,
    x_content_length: Union[Unset, int] = UNSET,
    upload_length: Union[Unset, int] = UNSET,
    tus_resumable: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]]:
    """upload artifact

     Upload content and create a artifacts.

    Args:
        content_type (Union[Unset, str]): Content-Type header, MUST define type of uploaded
            content. Example: application/x-netcdf4.
        content_encoding (Union[Unset, str]): Content-Encoding header, MAY define encoding of
            content. Example: gzip.
        content_length (Union[Unset, int]): Content-Length header, MAY define size of expected
            upload. Example: 2376.
        x_name (Union[Unset, str]): X-Name header, MAY define a more human friendly name. Reusing
            a name will NOT override an existing artifact with the same name Example: field-trip-
            jun-22.
        x_collection (Union[Unset, str]): X-Collection header, MAY define an collection name as a
            simple way of grouping artifacts Example: field-trip-jun-22.
        x_content_type (Union[Unset, str]): X-Content-Type header, used for initial, empty content
            creation requests. Example: application/x-netcdf4.
        x_content_length (Union[Unset, int]): X-Content-Length header, used for initial, empty
            content creation requests. Example: 2376.
        upload_length (Union[Unset, int]): Upload-Length header, sets the expected content size
            part of the TUS protocol. Example: 2376.
        tus_resumable (Union[Unset, str]): Tus-Resumable header, specifies TUS protocol version.
            Example: 1.0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ArtifactStatusRT, InvalidScopesT, NotImplementedT]
    """

    return (
        await asyncio_detailed(
            client=client,
            content_type=content_type,
            content_encoding=content_encoding,
            content_length=content_length,
            x_name=x_name,
            x_collection=x_collection,
            x_content_type=x_content_type,
            x_content_length=x_content_length,
            upload_length=upload_length,
            tus_resumable=tus_resumable,
        )
    ).parsed
