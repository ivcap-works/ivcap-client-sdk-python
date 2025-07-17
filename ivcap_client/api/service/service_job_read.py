from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.job_status_rt import JobStatusRT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, Response, Unset


def _get_kwargs(
    service_id: str,
    id: str,
    *,
    with_request_content: Union[Unset, None, bool] = UNSET,
    with_result_content: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["with-request-content"] = with_request_content

    params["with-result-content"] = with_result_content

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/1/services2/{service_id}/jobs/{id}".format(
            service_id=service_id,
            id=id,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = JobStatusRT.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = BadRequestT.from_dict(response.json())

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
) -> Response[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    with_request_content: Union[Unset, None, bool] = UNSET,
    with_result_content: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    """job-read service

     show the status of a job within the context of a service

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:services.
        id (str): ID of job to show Example: urn:ivcap:job.
        with_request_content (Union[Unset, None, bool]): include request content if possible
            Example: True.
        with_result_content (Union[Unset, None, bool]): include result content if possible

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        id=id,
        with_request_content=with_request_content,
        with_result_content=with_result_content,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    with_request_content: Union[Unset, None, bool] = UNSET,
    with_result_content: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    """job-read service

     show the status of a job within the context of a service

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:services.
        id (str): ID of job to show Example: urn:ivcap:job.
        with_request_content (Union[Unset, None, bool]): include request content if possible
            Example: True.
        with_result_content (Union[Unset, None, bool]): include result content if possible

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]
    """

    return sync_detailed(
        service_id=service_id,
        id=id,
        client=client,
        with_request_content=with_request_content,
        with_result_content=with_result_content,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    with_request_content: Union[Unset, None, bool] = UNSET,
    with_result_content: Union[Unset, None, bool] = UNSET,
) -> Response[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    """job-read service

     show the status of a job within the context of a service

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:services.
        id (str): ID of job to show Example: urn:ivcap:job.
        with_request_content (Union[Unset, None, bool]): include request content if possible
            Example: True.
        with_result_content (Union[Unset, None, bool]): include result content if possible

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        id=id,
        with_request_content=with_request_content,
        with_result_content=with_result_content,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    id: str,
    *,
    client: AuthenticatedClient,
    with_request_content: Union[Unset, None, bool] = UNSET,
    with_result_content: Union[Unset, None, bool] = UNSET,
) -> Optional[Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]]:
    """job-read service

     show the status of a job within the context of a service

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:services.
        id (str): ID of job to show Example: urn:ivcap:job.
        with_request_content (Union[Unset, None, bool]): include request content if possible
            Example: True.
        with_result_content (Union[Unset, None, bool]): include result content if possible

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BadRequestT, InvalidScopesT, JobStatusRT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            id=id,
            client=client,
            with_request_content=with_request_content,
            with_result_content=with_result_content,
        )
    ).parsed
