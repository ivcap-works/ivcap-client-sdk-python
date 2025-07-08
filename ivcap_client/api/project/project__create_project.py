from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.project_create_request import ProjectCreateRequest
from ...models.project_status_rt import ProjectStatusRT
from ...types import Response


def _get_kwargs(
    *,
    body: ProjectCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/project",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    if response.status_code == 200:
        response_200 = ProjectStatusRT.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequest,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    """Create a Project

     Create a new project and return its status.

    Args:
        body (ProjectCreateRequest):  Example: {'account_urn':
            'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name',
            'parent_project_urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1',
            'properties': {'details': 'Created for to investigate [objective]'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]
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
    body: ProjectCreateRequest,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    """Create a Project

     Create a new project and return its status.

    Args:
        body (ProjectCreateRequest):  Example: {'account_urn':
            'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name',
            'parent_project_urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1',
            'properties': {'details': 'Created for to investigate [objective]'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequest,
) -> Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    """Create a Project

     Create a new project and return its status.

    Args:
        body (ProjectCreateRequest):  Example: {'account_urn':
            'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name',
            'parent_project_urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1',
            'properties': {'details': 'Created for to investigate [objective]'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequest,
) -> Optional[Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]]:
    """Create a Project

     Create a new project and return its status.

    Args:
        body (ProjectCreateRequest):  Example: {'account_urn':
            'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name',
            'parent_project_urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1',
            'properties': {'details': 'Created for to investigate [objective]'}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidParameterT, InvalidScopesT, ProjectStatusRT]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
