from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

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
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/1/services",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ResourceNotFoundT, ServiceStatusRT]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ServiceStatusRT.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = ResourceNotFoundT.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterT.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.FAILED_DEPENDENCY:
        response_424 = BadRequestT.from_dict(response.json())

        return response_424
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = BadRequestT.from_dict(response.json())

        return response_501
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
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
    """create_service service

     Create a new services and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'banner': 'http://brakus.com/aleen_mohr',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}], 'tags': ['tag1', 'tag2'],
            'workflow': {'argo': 'Quidem nulla quae provident dolor amet nulla.', 'basic': {'command':
            ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-
            storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-
            tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Et aut autem deserunt sit
            architecto.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'},
            'type': 'basic'}}.

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
    """create_service service

     Create a new services and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'banner': 'http://brakus.com/aleen_mohr',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}], 'tags': ['tag1', 'tag2'],
            'workflow': {'argo': 'Quidem nulla quae provident dolor amet nulla.', 'basic': {'command':
            ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-
            storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-
            tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Et aut autem deserunt sit
            architecto.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'},
            'type': 'basic'}}.

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
    """create_service service

     Create a new services and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'banner': 'http://brakus.com/aleen_mohr',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}], 'tags': ['tag1', 'tag2'],
            'workflow': {'argo': 'Quidem nulla quae provident dolor amet nulla.', 'basic': {'command':
            ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-
            storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-
            tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Et aut autem deserunt sit
            architecto.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'},
            'type': 'basic'}}.

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
    """create_service service

     Create a new services and return its status.

    Args:
        body (ServiceDefinitionT):  Example: {'banner': 'http://brakus.com/aleen_mohr',
            'description': 'This service ...', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name',
            'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name':
            'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}, {'title': 'Ipsa
            perspiciatis esse rerum.', 'uri': 'http://gulgowski.biz/kyle'}], 'tags': ['tag1', 'tag2'],
            'workflow': {'argo': 'Quidem nulla quae provident dolor amet nulla.', 'basic': {'command':
            ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-
            storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-
            tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Et aut autem deserunt sit
            architecto.', 'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'},
            'type': 'basic'}}.

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
