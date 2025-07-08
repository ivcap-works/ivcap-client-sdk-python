from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.service_definition_t import ServiceDefinitionT
from ...models.service_status_rt import ServiceStatusRT
from ...types import Response


def _get_kwargs(
    *,
    body: ServiceDefinitionT,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/services2",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    if response.status_code == 201:
        response_201 = ServiceStatusRT.from_dict(response.json())

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
    if response.status_code == 404:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ServiceDefinitionT,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    """service-create service

     Create a new service and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'controller': [{'$schema':
            'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'], 'image':
            'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits':
            {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m',
            'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}], 'controller-schema':
            'urn:ivcap:schema.service.argo.1', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label':
            'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold',
            'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]
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
    body: ServiceDefinitionT,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    """service-create service

     Create a new service and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'controller': [{'$schema':
            'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'], 'image':
            'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits':
            {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m',
            'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}], 'controller-schema':
            'urn:ivcap:schema.service.argo.1', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label':
            'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold',
            'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ServiceDefinitionT,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    """service-create service

     Create a new service and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'controller': [{'$schema':
            'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'], 'image':
            'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits':
            {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m',
            'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}], 'controller-schema':
            'urn:ivcap:schema.service.argo.1', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label':
            'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold',
            'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ServiceDefinitionT,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    """service-create service

     Create a new service and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'controller': [{'$schema':
            'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'], 'image':
            'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits':
            {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m',
            'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}], 'controller-schema':
            'urn:ivcap:schema.service.argo.1', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label':
            'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold',
            'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
