from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.secret_result_t import SecretResultT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    secret_name: str,
    secret_type: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["secret-name"] = secret_name

    params["secret-type"] = secret_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/secrets",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    if response.status_code == 200:
        response_200 = SecretResultT.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    secret_name: str,
    secret_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    """get secret

     Get a secrets

    Args:
        secret_name (str): Secret name Example: test-purpose-secret.
        secret_type (Union[Unset, str]): Secret type Example: raw.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]
    """

    kwargs = _get_kwargs(
        secret_name=secret_name,
        secret_type=secret_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    secret_name: str,
    secret_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    """get secret

     Get a secrets

    Args:
        secret_name (str): Secret name Example: test-purpose-secret.
        secret_type (Union[Unset, str]): Secret type Example: raw.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]
    """

    return sync_detailed(
        client=client,
        secret_name=secret_name,
        secret_type=secret_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    secret_name: str,
    secret_type: Union[Unset, str] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    """get secret

     Get a secrets

    Args:
        secret_name (str): Secret name Example: test-purpose-secret.
        secret_type (Union[Unset, str]): Secret type Example: raw.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]
    """

    kwargs = _get_kwargs(
        secret_name=secret_name,
        secret_type=secret_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    secret_name: str,
    secret_type: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]]:
    """get secret

     Get a secrets

    Args:
        secret_name (str): Secret name Example: test-purpose-secret.
        secret_type (Union[Unset, str]): Secret type Example: raw.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, SecretResultT]
    """

    return (
        await asyncio_detailed(
            client=client,
            secret_name=secret_name,
            secret_type=secret_type,
        )
    ).parsed
