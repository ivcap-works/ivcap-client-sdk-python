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
    id: str,
    *,
    body: File,
    entity_id: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    policy_id: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(content_type, Unset):
        headers["Content-Type"] = content_type

    params: dict[str, Any] = {}

    params["entity-id"] = entity_id

    params["schema"] = schema

    params["policy-id"] = policy_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/1/metadata/{id}",
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
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    policy_id: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """update_record metadata

     Revoke this record and create a new one with the information provided.
                        For any field not provided, the value from the current record is used.

    Args:
        id (str): Record ID to update Example:
            urn:ivcap:record.53cbb715-4ffd-4158-9e55-5d0ae69605a4.
        entity_id (Union[Unset, str]): Entity to which attach metadata Example: urn:url:.....
        schema (Union[Unset, str]): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://spencerwindler.biz/chandler.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        id=id,
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
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    policy_id: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """update_record metadata

     Revoke this record and create a new one with the information provided.
                        For any field not provided, the value from the current record is used.

    Args:
        id (str): Record ID to update Example:
            urn:ivcap:record.53cbb715-4ffd-4158-9e55-5d0ae69605a4.
        entity_id (Union[Unset, str]): Entity to which attach metadata Example: urn:url:.....
        schema (Union[Unset, str]): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://spencerwindler.biz/chandler.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    policy_id: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """update_record metadata

     Revoke this record and create a new one with the information provided.
                        For any field not provided, the value from the current record is used.

    Args:
        id (str): Record ID to update Example:
            urn:ivcap:record.53cbb715-4ffd-4158-9e55-5d0ae69605a4.
        entity_id (Union[Unset, str]): Entity to which attach metadata Example: urn:url:.....
        schema (Union[Unset, str]): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://spencerwindler.biz/chandler.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    entity_id: Union[Unset, str] = UNSET,
    schema: Union[Unset, str] = UNSET,
    policy_id: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]]:
    """update_record metadata

     Revoke this record and create a new one with the information provided.
                        For any field not provided, the value from the current record is used.

    Args:
        id (str): Record ID to update Example:
            urn:ivcap:record.53cbb715-4ffd-4158-9e55-5d0ae69605a4.
        entity_id (Union[Unset, str]): Entity to which attach metadata Example: urn:url:.....
        schema (Union[Unset, str]): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, str]): Policy guiding visibility and actions performed Example:
            http://spencerwindler.biz/chandler.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, BadRequestT, InvalidParameterT, InvalidScopesT]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            entity_id=entity_id,
            schema=schema,
            policy_id=policy_id,
            content_type=content_type,
        )
    ).parsed
