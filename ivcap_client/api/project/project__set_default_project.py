from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.set_default_project_request_body import SetDefaultProjectRequestBody
from ...types import Response


def _get_kwargs(
    *,
    body: SetDefaultProjectRequestBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/1/project/default",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 400:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SetDefaultProjectRequestBody,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """Set User's Default Project

     Sets the default project of a user.

    Args:
        body (SetDefaultProjectRequestBody):  Example: {'project_urn':
            'urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f', 'user_urn':
            'urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: SetDefaultProjectRequestBody,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """Set User's Default Project

     Sets the default project of a user.

    Args:
        body (SetDefaultProjectRequestBody):  Example: {'project_urn':
            'urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f', 'user_urn':
            'urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SetDefaultProjectRequestBody,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """Set User's Default Project

     Sets the default project of a user.

    Args:
        body (SetDefaultProjectRequestBody):  Example: {'project_urn':
            'urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f', 'user_urn':
            'urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SetDefaultProjectRequestBody,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """Set User's Default Project

     Sets the default project of a user.

    Args:
        body (SetDefaultProjectRequestBody):  Example: {'project_urn':
            'urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f', 'user_urn':
            'urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
