from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_meta_rt import AddMetaRT
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    json_body: Dict,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers = {}
    if not isinstance(content_type, Unset):
        headers["Content-Type"] = content_type

    params: Dict[str, Any] = {}
    params["entity-id"] = entity_id

    params["schema"] = schema

    params["policy-id"] = policy_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body

    return {
        "method": "put",
        "url": "/1/metadata",
        "json": json_json_body,
        "params": params,
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AddMetaRT.from_dict(response.json())

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
) -> Response[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Dict,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    """update_one metadata

     Revoke a record for the same entity and same schema and create new one
                        with the provided properties. __NOTE__, this method will fail if there is more than one active
    record for the entity/schema pair.

    Args:
        entity_id (str): Entity to which attach metadata Example: urn:url:.....
        schema (str): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, None, str]): Policy guiding visibility and actions performed
            Example: http://heidenreich.org/maximus.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        json_body (Dict): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
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
    json_body: Dict,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    """update_one metadata

     Revoke a record for the same entity and same schema and create new one
                        with the provided properties. __NOTE__, this method will fail if there is more than one active
    record for the entity/schema pair.

    Args:
        entity_id (str): Entity to which attach metadata Example: urn:url:.....
        schema (str): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, None, str]): Policy guiding visibility and actions performed
            Example: http://heidenreich.org/maximus.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        json_body (Dict): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        entity_id=entity_id,
        schema=schema,
        policy_id=policy_id,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: Dict,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    """update_one metadata

     Revoke a record for the same entity and same schema and create new one
                        with the provided properties. __NOTE__, this method will fail if there is more than one active
    record for the entity/schema pair.

    Args:
        entity_id (str): Entity to which attach metadata Example: urn:url:.....
        schema (str): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, None, str]): Policy guiding visibility and actions performed
            Example: http://heidenreich.org/maximus.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        json_body (Dict): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
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
    json_body: Dict,
    entity_id: str,
    schema: str,
    policy_id: Union[Unset, None, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]]:
    """update_one metadata

     Revoke a record for the same entity and same schema and create new one
                        with the provided properties. __NOTE__, this method will fail if there is more than one active
    record for the entity/schema pair.

    Args:
        entity_id (str): Entity to which attach metadata Example: urn:url:.....
        schema (str): Schema of metadata Example: urn:url:.....
        policy_id (Union[Unset, None, str]): Policy guiding visibility and actions performed
            Example: http://heidenreich.org/maximus.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        json_body (Dict): Aspect content Example: {"$schema": ...}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddMetaRT, Any, InvalidParameterValue, InvalidScopesT, NotImplementedT]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            entity_id=entity_id,
            schema=schema,
            policy_id=policy_id,
            content_type=content_type,
        )
    ).parsed
