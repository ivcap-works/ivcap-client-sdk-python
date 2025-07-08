from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.messagestatus import Messagestatus
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    id: str,
    *,
    body: File,
    schema: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(content_type, Unset):
        headers["Content-Type"] = content_type

    params: dict[str, Any] = {}

    params["schema"] = schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/1/queues/{id}/messages",
        "params": params,
    }

    _body = body.to_tuple()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
    if response.status_code == 200:
        response_200 = Messagestatus.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
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
    schema: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
    """enqueue queue

     Send a message to a specific queues.

    Args:
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema used for message Example:
            urn:ivcap:schema:queue:message.1.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Message content Example: {"temperature": "21", "location": "Buoy101",
            "timestamp": "2024-05-20T14:30:00Z"}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        schema=schema,
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
    schema: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
    """enqueue queue

     Send a message to a specific queues.

    Args:
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema used for message Example:
            urn:ivcap:schema:queue:message.1.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Message content Example: {"temperature": "21", "location": "Buoy101",
            "timestamp": "2024-05-20T14:30:00Z"}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        schema=schema,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    schema: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
    """enqueue queue

     Send a message to a specific queues.

    Args:
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema used for message Example:
            urn:ivcap:schema:queue:message.1.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Message content Example: {"temperature": "21", "location": "Buoy101",
            "timestamp": "2024-05-20T14:30:00Z"}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        schema=schema,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: File,
    schema: Union[Unset, str] = UNSET,
    content_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]]:
    """enqueue queue

     Send a message to a specific queues.

    Args:
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema used for message Example:
            urn:ivcap:schema:queue:message.1.
        content_type (Union[Unset, str]): Content-Type header, MUST be of application/json.
            Example: application/json.
        body (File): Message content Example: {"temperature": "21", "location": "Buoy101",
            "timestamp": "2024-05-20T14:30:00Z"}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, Messagestatus]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            schema=schema,
            content_type=content_type,
        )
    ).parsed
