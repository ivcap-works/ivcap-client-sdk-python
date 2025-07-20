from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.push_status_t import PushStatusT
from ...types import UNSET, Response


def _get_kwargs(
    *,
    tag: str,
    digest: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["tag"] = tag

    params["digest"] = digest

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/1/packages/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    if response.status_code == 200:
        response_200 = PushStatusT.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    tag: str,
    digest: str,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    """status package

     check push status of a layer

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        digest (str): docker image layer digest Example:
            sha256@6d516395bac7b1774e648a6196fbed7589efbe2c479831ee042fca0cf52ce61f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        digest=digest,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    tag: str,
    digest: str,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    """status package

     check push status of a layer

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        digest (str): docker image layer digest Example:
            sha256@6d516395bac7b1774e648a6196fbed7589efbe2c479831ee042fca0cf52ce61f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]
    """

    return sync_detailed(
        client=client,
        tag=tag,
        digest=digest,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    tag: str,
    digest: str,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    """status package

     check push status of a layer

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        digest (str): docker image layer digest Example:
            sha256@6d516395bac7b1774e648a6196fbed7589efbe2c479831ee042fca0cf52ce61f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        digest=digest,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    tag: str,
    digest: str,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]]:
    """status package

     check push status of a layer

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        digest (str): docker image layer digest Example:
            sha256@6d516395bac7b1774e648a6196fbed7589efbe2c479831ee042fca0cf52ce61f.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushStatusT]
    """

    return (
        await asyncio_detailed(
            client=client,
            tag=tag,
            digest=digest,
        )
    ).parsed
