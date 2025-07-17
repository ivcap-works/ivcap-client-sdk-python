from http import HTTPStatus
from io import BytesIO
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.job_retry_later_t import JobRetryLaterT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    content_type: str,
    ivcap_order_id: Union[Unset, str] = UNSET,
    x_forwarded_host: Union[Unset, str] = UNSET,
    x_forwarded_proto: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    headers = {}
    headers["Content-Type"] = content_type

    if not isinstance(ivcap_order_id, Unset):
        headers["IVCAP-Order-Id"] = ivcap_order_id

    if not isinstance(x_forwarded_host, Unset):
        headers["X-Forwarded-Host"] = x_forwarded_host

    if not isinstance(x_forwarded_proto, Unset):
        headers["X-Forwarded-Proto"] = x_forwarded_proto

    if not isinstance(timeout, Unset):
        headers["Timeout"] = str(timeout)

    return {
        "method": "post",
        "url": "/1/services2/{service_id}/jobs".format(
            service_id=service_id,
        ),
        "headers": headers,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200
    if response.status_code == HTTPStatus.ACCEPTED:
        response_202 = JobRetryLaterT.from_dict(response.json())

        return response_202
    if response.status_code == HTTPStatus.TEMPORARY_REDIRECT:
        response_307 = File(payload=BytesIO(response.json()))

        return response_307
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
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient,
    content_type: str,
    ivcap_order_id: Union[Unset, str] = UNSET,
    x_forwarded_host: Union[Unset, str] = UNSET,
    x_forwarded_proto: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Dolore assumenda tenetur..
        ivcap_order_id (Union[Unset, str]):  Example: Eos soluta modi aut et..
        x_forwarded_host (Union[Unset, str]):  Example: Illo dolores inventore odit unde
            architecto quis..
        x_forwarded_proto (Union[Unset, str]):  Example: Et porro ducimus corporis quas..
        timeout (Union[Unset, int]):  Example: 2288004455320260932.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        content_type=content_type,
        ivcap_order_id=ivcap_order_id,
        x_forwarded_host=x_forwarded_host,
        x_forwarded_proto=x_forwarded_proto,
        timeout=timeout,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    service_id: str,
    *,
    client: AuthenticatedClient,
    content_type: str,
    ivcap_order_id: Union[Unset, str] = UNSET,
    x_forwarded_host: Union[Unset, str] = UNSET,
    x_forwarded_proto: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Dolore assumenda tenetur..
        ivcap_order_id (Union[Unset, str]):  Example: Eos soluta modi aut et..
        x_forwarded_host (Union[Unset, str]):  Example: Illo dolores inventore odit unde
            architecto quis..
        x_forwarded_proto (Union[Unset, str]):  Example: Et porro ducimus corporis quas..
        timeout (Union[Unset, int]):  Example: 2288004455320260932.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        content_type=content_type,
        ivcap_order_id=ivcap_order_id,
        x_forwarded_host=x_forwarded_host,
        x_forwarded_proto=x_forwarded_proto,
        timeout=timeout,
    ).parsed


async def asyncio_detailed(
    service_id: str,
    *,
    client: AuthenticatedClient,
    content_type: str,
    ivcap_order_id: Union[Unset, str] = UNSET,
    x_forwarded_host: Union[Unset, str] = UNSET,
    x_forwarded_proto: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
) -> Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Dolore assumenda tenetur..
        ivcap_order_id (Union[Unset, str]):  Example: Eos soluta modi aut et..
        x_forwarded_host (Union[Unset, str]):  Example: Illo dolores inventore odit unde
            architecto quis..
        x_forwarded_proto (Union[Unset, str]):  Example: Et porro ducimus corporis quas..
        timeout (Union[Unset, int]):  Example: 2288004455320260932.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        content_type=content_type,
        ivcap_order_id=ivcap_order_id,
        x_forwarded_host=x_forwarded_host,
        x_forwarded_proto=x_forwarded_proto,
        timeout=timeout,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    service_id: str,
    *,
    client: AuthenticatedClient,
    content_type: str,
    ivcap_order_id: Union[Unset, str] = UNSET,
    x_forwarded_host: Union[Unset, str] = UNSET,
    x_forwarded_proto: Union[Unset, str] = UNSET,
    timeout: Union[Unset, int] = UNSET,
) -> Optional[Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Dolore assumenda tenetur..
        ivcap_order_id (Union[Unset, str]):  Example: Eos soluta modi aut et..
        x_forwarded_host (Union[Unset, str]):  Example: Illo dolores inventore odit unde
            architecto quis..
        x_forwarded_proto (Union[Unset, str]):  Example: Et porro ducimus corporis quas..
        timeout (Union[Unset, int]):  Example: 2288004455320260932.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BadRequestT, File, InvalidParameterT, InvalidScopesT, JobRetryLaterT, ResourceNotFoundT]
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            content_type=content_type,
            ivcap_order_id=ivcap_order_id,
            x_forwarded_host=x_forwarded_host,
            x_forwarded_proto=x_forwarded_proto,
            timeout=timeout,
        )
    ).parsed
