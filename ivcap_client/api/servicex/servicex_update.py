from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.x_service_definition_t import XServiceDefinitionT
from ...models.x_service_status_rt import XServiceStatusRT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    body: XServiceDefinitionT,
    force_create: bool | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["force-create"] = force_create

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/1/services/{id}".format(
            id=quote(str(id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    Any
    | BadRequestT
    | InvalidParameterT
    | InvalidScopesT
    | NotImplementedT
    | ResourceNotFoundT
    | XServiceStatusRT
    | None
):
    if response.status_code == 200:
        response_200 = XServiceStatusRT.from_dict(response.json())

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
        response_501 = NotImplementedT.from_dict(response.json())

        return response_501

    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT
]:
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
    body: XServiceDefinitionT,
    force_create: bool | Unset = UNSET,
) -> Response[
    Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT
]:
    """update servicex

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Rerum sit..
        force_create (bool | Unset): Create if not already exist Example: True.
        body (XServiceDefinitionT):  Example: {'banner': 'http://rice.biz/rickie_christiansen',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Eius
            officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}, {'title':
            'Eius officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}],
            'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et quia quis ut quia.', 'basic':
            {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'},
            'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
            'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Aliquam qui qui voluptates
            quo.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type':
            'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        force_create=force_create,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: XServiceDefinitionT,
    force_create: bool | Unset = UNSET,
) -> (
    Any
    | BadRequestT
    | InvalidParameterT
    | InvalidScopesT
    | NotImplementedT
    | ResourceNotFoundT
    | XServiceStatusRT
    | None
):
    """update servicex

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Rerum sit..
        force_create (bool | Unset): Create if not already exist Example: True.
        body (XServiceDefinitionT):  Example: {'banner': 'http://rice.biz/rickie_christiansen',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Eius
            officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}, {'title':
            'Eius officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}],
            'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et quia quis ut quia.', 'basic':
            {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'},
            'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
            'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Aliquam qui qui voluptates
            quo.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type':
            'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
        force_create=force_create,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: XServiceDefinitionT,
    force_create: bool | Unset = UNSET,
) -> Response[
    Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT
]:
    """update servicex

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Rerum sit..
        force_create (bool | Unset): Create if not already exist Example: True.
        body (XServiceDefinitionT):  Example: {'banner': 'http://rice.biz/rickie_christiansen',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Eius
            officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}, {'title':
            'Eius officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}],
            'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et quia quis ut quia.', 'basic':
            {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'},
            'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
            'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Aliquam qui qui voluptates
            quo.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type':
            'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
        force_create=force_create,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: XServiceDefinitionT,
    force_create: bool | Unset = UNSET,
) -> (
    Any
    | BadRequestT
    | InvalidParameterT
    | InvalidScopesT
    | NotImplementedT
    | ResourceNotFoundT
    | XServiceStatusRT
    | None
):
    """update servicex

     Update an existing services and return its status.

    Args:
        id (str): ID of services to update Example: Rerum sit..
        force_create (bool | Unset): Create if not already exist Example: True.
        body (XServiceDefinitionT):  Example: {'banner': 'http://rice.biz/rickie_christiansen',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Eius
            officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}, {'title':
            'Eius officiis enim quam blanditiis soluta.', 'uri': 'http://reinger.name/wiley'}],
            'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et quia quis ut quia.', 'basic':
            {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'},
            'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
            'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Aliquam qui qui voluptates
            quo.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type':
            'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | BadRequestT | InvalidParameterT | InvalidScopesT | NotImplementedT | ResourceNotFoundT | XServiceStatusRT
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
            force_create=force_create,
        )
    ).parsed
