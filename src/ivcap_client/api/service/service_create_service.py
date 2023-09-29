from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.invalid_parameter_value import InvalidParameterValue
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.not_implemented_t import NotImplementedT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...models.service_description_t import ServiceDescriptionT
from ...models.service_status_rt import ServiceStatusRT
from ...types import Response


def _get_kwargs(
    *,
    json_body: ServiceDescriptionT,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/1/services",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = ServiceStatusRT.from_dict(response.json())

        return response_201
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
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
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """create_service service

     Create a new services and return its status.

    Args:
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """create_service service

     Create a new services and return its status.

    Args:
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
) -> Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """create_service service

     Create a new services and return its status.

    Args:
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: ServiceDescriptionT,
) -> Optional[Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]]:
    """create_service service

     Create a new services and return its status.

    Args:
        json_body (ServiceDescriptionT):  Example: {'account-id':
            'urn:ivcap:account:0f0e3f57-80f7-4899-9b69-459af2efd789', 'banner':
            'http://hoeger.biz/alisa.dare', 'description': 'This service ...', 'metadata': [{'name':
            'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis voluptatem.'},
            {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla facilis
            voluptatem.'}, {'name': 'Vel cupiditate iure beatae libero.', 'value': 'Culpa nulla
            facilis voluptatem.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The
            name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float',
            'unit': 'm'}], 'policy-id': 'Dolore nemo.', 'provider-id':
            'urn:ivcap:provider:0f0e3f57-80f7-4899-9b69-459af2efd789', 'provider-ref':
            'service_foo_patch_1', 'references': [{'title': 'Eius perferendis culpa voluptates fuga
            dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius perferendis culpa
            voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'}, {'title': 'Eius
            perferendis culpa voluptates fuga dicta.', 'uri': 'http://dach.name/candace.king'},
            {'title': 'Eius perferendis culpa voluptates fuga dicta.', 'uri':
            'http://dach.name/candace.king'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Et
            perferendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit':
            '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'},
            'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}, 'opts': 'Maxime eius
            voluptatibus tempore assumenda et qui.', 'type': 'basic'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, InvalidParameterValue, InvalidScopesT, NotImplementedT, ResourceNotFoundT, ServiceStatusRT]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
