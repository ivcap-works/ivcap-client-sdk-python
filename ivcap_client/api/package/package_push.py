from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.packagepush_type import PackagepushType
from ...models.push_response_body import PushResponseBody
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    tag: str,
    force: Union[Unset, bool] = UNSET,
    type_: PackagepushType,
    digest: str,
    total: Union[Unset, int] = UNSET,
    start: Union[Unset, int] = UNSET,
    end: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["tag"] = tag

    params["force"] = force

    json_type_ = type_.value
    params["type"] = json_type_

    params["digest"] = digest

    params["total"] = total

    params["start"] = start

    params["end"] = end

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/packages/push",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
    if response.status_code == 201:
        response_201 = PushResponseBody.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == 409:
        response_409 = ResourceNotFoundT.from_dict(response.json())

        return response_409
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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
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
    force: Union[Unset, bool] = UNSET,
    type_: PackagepushType,
    digest: str,
    total: Union[Unset, int] = UNSET,
    start: Union[Unset, int] = UNSET,
    end: Union[Unset, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
    """push package

     upload service's docker image to container registry

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        force (Union[Unset, bool]): force to override Example: True.
        type_ (PackagepushType): push type, either be manifest, config or layer Example: layer.
        digest (str): digest of the push Example:
            sha:209820a1b307ce3ab81b7f2a944224159259b580eb94e96ab30fc4683f5b96a1.
        total (Union[Unset, int]): total size of the layer Example: 102403457.
        start (Union[Unset, int]): start of the layer chunk
        end (Union[Unset, int]): end of the layer chunk Example: 10240.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        force=force,
        type_=type_,
        digest=digest,
        total=total,
        start=start,
        end=end,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    tag: str,
    force: Union[Unset, bool] = UNSET,
    type_: PackagepushType,
    digest: str,
    total: Union[Unset, int] = UNSET,
    start: Union[Unset, int] = UNSET,
    end: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
    """push package

     upload service's docker image to container registry

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        force (Union[Unset, bool]): force to override Example: True.
        type_ (PackagepushType): push type, either be manifest, config or layer Example: layer.
        digest (str): digest of the push Example:
            sha:209820a1b307ce3ab81b7f2a944224159259b580eb94e96ab30fc4683f5b96a1.
        total (Union[Unset, int]): total size of the layer Example: 102403457.
        start (Union[Unset, int]): start of the layer chunk
        end (Union[Unset, int]): end of the layer chunk Example: 10240.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]
    """

    return sync_detailed(
        client=client,
        tag=tag,
        force=force,
        type_=type_,
        digest=digest,
        total=total,
        start=start,
        end=end,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    tag: str,
    force: Union[Unset, bool] = UNSET,
    type_: PackagepushType,
    digest: str,
    total: Union[Unset, int] = UNSET,
    start: Union[Unset, int] = UNSET,
    end: Union[Unset, int] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
    """push package

     upload service's docker image to container registry

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        force (Union[Unset, bool]): force to override Example: True.
        type_ (PackagepushType): push type, either be manifest, config or layer Example: layer.
        digest (str): digest of the push Example:
            sha:209820a1b307ce3ab81b7f2a944224159259b580eb94e96ab30fc4683f5b96a1.
        total (Union[Unset, int]): total size of the layer Example: 102403457.
        start (Union[Unset, int]): start of the layer chunk
        end (Union[Unset, int]): end of the layer chunk Example: 10240.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        tag=tag,
        force=force,
        type_=type_,
        digest=digest,
        total=total,
        start=start,
        end=end,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    tag: str,
    force: Union[Unset, bool] = UNSET,
    type_: PackagepushType,
    digest: str,
    total: Union[Unset, int] = UNSET,
    start: Union[Unset, int] = UNSET,
    end: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]]:
    """push package

     upload service's docker image to container registry

    Args:
        tag (str): docker image tag Example: test_app:1.0.1.
        force (Union[Unset, bool]): force to override Example: True.
        type_ (PackagepushType): push type, either be manifest, config or layer Example: layer.
        digest (str): digest of the push Example:
            sha:209820a1b307ce3ab81b7f2a944224159259b580eb94e96ab30fc4683f5b96a1.
        total (Union[Unset, int]): total size of the layer Example: 102403457.
        start (Union[Unset, int]): start of the layer chunk
        end (Union[Unset, int]): end of the layer chunk Example: 10240.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, PushResponseBody, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            client=client,
            tag=tag,
            force=force,
            type_=type_,
            digest=digest,
            total=total,
            start=start,
            end=end,
        )
    ).parsed
