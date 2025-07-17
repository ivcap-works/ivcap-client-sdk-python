from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import File, Response


def _get_kwargs(
    service_id: str,
    job_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/1/services2/{service_id}/jobs/{job_id}/output".format(
            service_id=service_id,
            job_id=job_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if response.status_code == HTTPStatus.NO_CONTENT:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = File(payload=BytesIO(response.json()))

        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = InvalidScopesT.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ResourceNotFoundT.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = InvalidParameterT.from_dict(response.json())

        return response_422
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = BadRequestT.from_dict(response.json())

        return response_500
    if response.status_code == HTTPStatus.NOT_IMPLEMENTED:
        response_501 = BadRequestT.from_dict(response.json())

        return response_501
    if response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        response_503 = File(payload=BytesIO(response.json()))

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """job-output service

     Return the result of a job.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        job_id (str): ID of job for this service Example: urn:ivcap:job:....

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        job_id=job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """job-output service

     Return the result of a job.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        job_id (str): ID of job for this service Example: urn:ivcap:job:....

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return sync_detailed(
        service_id=service_id,
        job_id=job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """job-output service

     Return the result of a job.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        job_id (str): ID of job for this service Example: urn:ivcap:job:....

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        job_id=job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    job_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]]:
    """job-output service

     Return the result of a job.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        job_id (str): ID of job for this service Example: urn:ivcap:job:....

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, File, InvalidParameterT, InvalidScopesT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            job_id=job_id,
            client=client,
        )
    ).parsed
