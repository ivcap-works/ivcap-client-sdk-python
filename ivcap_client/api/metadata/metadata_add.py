from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_meta_rt import AddMetaRT
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    body: File,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, str] = UNSET,
    content_type: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Content-Type"] = content_type

    params: dict[str, Any] = {}

    params["entity-id"] = entity_id

    params["schema"] = schema

    params["policy-id"] = policy_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/metadata",
        "params": params,
    }

    _body = body.to_tuple()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    if response.status_code == 200:
        response_200 = AddMetaRT.from_dict(response.json())

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
) -> Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
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
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, str] = UNSET,
    content_type: str,
) -> Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """add metadata

     Attach new metadata to an entity.

    Args:
        entity_id (str): Entity to which attach metadata Example: http://welchsporer.name/brycen.
        schema (str): Schema of metadata Example: http://bins.net/paige.krajcik.
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://ledner.name/sigrid.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        body=body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
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
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, str] = UNSET,
    content_type: str,
) -> Optional[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """add metadata

     Attach new metadata to an entity.

    Args:
        entity_id (str): Entity to which attach metadata Example: http://welchsporer.name/brycen.
        schema (str): Schema of metadata Example: http://bins.net/paige.krajcik.
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://ledner.name/sigrid.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return sync_detailed(
        client=client,
        body=body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, str] = UNSET,
    content_type: str,
) -> Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """add metadata

     Attach new metadata to an entity.

    Args:
        entity_id (str): Entity to which attach metadata Example: http://welchsporer.name/brycen.
        schema (str): Schema of metadata Example: http://bins.net/paige.krajcik.
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://ledner.name/sigrid.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        body=body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, str] = UNSET,
    content_type: str,
) -> Optional[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """add metadata

     Attach new metadata to an entity.

    Args:
        entity_id (str): Entity to which attach metadata Example: http://welchsporer.name/brycen.
        schema (str): Schema of metadata Example: http://bins.net/paige.krajcik.
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://ledner.name/sigrid.
        content_type (str): Content-Type header, MUST be of application/json. Example:
            application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            entity_id=entity_id,
            schema=schema,
            policy_id=policy_id,
            content_type=content_type,
        )
    ).parsed
