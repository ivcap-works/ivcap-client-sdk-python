from http import HTTPStatus
from io import BytesIO
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bad_request_t import BadRequestT
from ...models.invalid_parameter_t import InvalidParameterT
from ...models.invalid_scopes_t import InvalidScopesT
from ...models.job_retry_later_t import JobRetryLaterT
from ...models.not_implemented_t import NotImplementedT
from ...models.resource_not_found_t import ResourceNotFoundT
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    service_id: str,
    *,
    body: Any,
    content_type: str,
    ivcap_order_id: str | Unset = UNSET,
    x_forwarded_host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,
    timeout: int | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Content-Type"] = content_type

    if not isinstance(ivcap_order_id, Unset):
        headers["IVCAP-Order-Id"] = ivcap_order_id

    if not isinstance(x_forwarded_host, Unset):
        headers["X-Forwarded-Host"] = x_forwarded_host

    if not isinstance(x_forwarded_proto, Unset):
        headers["X-Forwarded-Proto"] = x_forwarded_proto

    if not isinstance(timeout, Unset):
        headers["Timeout"] = str(timeout)

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/1/services2/{service_id}/jobs".format(
            service_id=quote(str(service_id), safe=""),
        ),
    }

    _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> (
    BadRequestT
    | File
    | InvalidParameterT
    | InvalidScopesT
    | JobRetryLaterT
    | NotImplementedT
    | ResourceNotFoundT
    | None
):
    if response.status_code == 200:
        response_200 = File(payload=BytesIO(response.json()))

        return response_200

    if response.status_code == 202:
        response_202 = JobRetryLaterT.from_dict(response.json())

        return response_202

    if response.status_code == 307:
        response_307 = File(payload=BytesIO(response.json()))

        return response_307

    if response.status_code == 400:
        response_400 = BadRequestT.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = File(payload=BytesIO(response.json()))

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
        response_503 = File(payload=BytesIO(response.json()))

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[
    BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT
]:
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
    body: Any,
    content_type: str,
    ivcap_order_id: str | Unset = UNSET,
    x_forwarded_host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,
    timeout: int | Unset = UNSET,
) -> Response[
    BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT
]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Nostrum tempora enim porro ex dolores..
        ivcap_order_id (str | Unset):  Example: Inventore officiis repellendus ipsum quasi harum
            vitae..
        x_forwarded_host (str | Unset):  Example: Vel vero..
        x_forwarded_proto (str | Unset):  Example: Nihil itaque quia..
        timeout (int | Unset):  Example: 2646310566242473292.
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
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
    body: Any,
    content_type: str,
    ivcap_order_id: str | Unset = UNSET,
    x_forwarded_host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,
    timeout: int | Unset = UNSET,
) -> (
    BadRequestT
    | File
    | InvalidParameterT
    | InvalidScopesT
    | JobRetryLaterT
    | NotImplementedT
    | ResourceNotFoundT
    | None
):
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Nostrum tempora enim porro ex dolores..
        ivcap_order_id (str | Unset):  Example: Inventore officiis repellendus ipsum quasi harum
            vitae..
        x_forwarded_host (str | Unset):  Example: Vel vero..
        x_forwarded_proto (str | Unset):  Example: Nihil itaque quia..
        timeout (int | Unset):  Example: 2646310566242473292.
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT
    """

    return sync_detailed(
        service_id=service_id,
        client=client,
        body=body,
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
    body: Any,
    content_type: str,
    ivcap_order_id: str | Unset = UNSET,
    x_forwarded_host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,
    timeout: int | Unset = UNSET,
) -> Response[
    BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT
]:
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Nostrum tempora enim porro ex dolores..
        ivcap_order_id (str | Unset):  Example: Inventore officiis repellendus ipsum quasi harum
            vitae..
        x_forwarded_host (str | Unset):  Example: Vel vero..
        x_forwarded_proto (str | Unset):  Example: Nihil itaque quia..
        timeout (int | Unset):  Example: 2646310566242473292.
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT]
    """

    kwargs = _get_kwargs(
        service_id=service_id,
        body=body,
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
    body: Any,
    content_type: str,
    ivcap_order_id: str | Unset = UNSET,
    x_forwarded_host: str | Unset = UNSET,
    x_forwarded_proto: str | Unset = UNSET,
    timeout: int | Unset = UNSET,
) -> (
    BadRequestT
    | File
    | InvalidParameterT
    | InvalidScopesT
    | JobRetryLaterT
    | NotImplementedT
    | ResourceNotFoundT
    | None
):
    """job-create service

     Create a job in the context of a specific service.

    Args:
        service_id (str): ID of service for which to show the list of jobs Example:
            urn:ivcap:service:....
        content_type (str):  Example: Nostrum tempora enim porro ex dolores..
        ivcap_order_id (str | Unset):  Example: Inventore officiis repellendus ipsum quasi harum
            vitae..
        x_forwarded_host (str | Unset):  Example: Vel vero..
        x_forwarded_proto (str | Unset):  Example: Nihil itaque quia..
        timeout (int | Unset):  Example: 2646310566242473292.
        body (Any):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BadRequestT | File | InvalidParameterT | InvalidScopesT | JobRetryLaterT | NotImplementedT | ResourceNotFoundT
    """

    return (
        await asyncio_detailed(
            service_id=service_id,
            client=client,
            body=body,
            content_type=content_type,
            ivcap_order_id=ivcap_order_id,
            x_forwarded_host=x_forwarded_host,
            x_forwarded_proto=x_forwarded_proto,
            timeout=timeout,
        )
    ).parsed
