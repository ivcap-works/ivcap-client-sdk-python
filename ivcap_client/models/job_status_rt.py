import datetime
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status_rt_status import JobStatusRTStatus
from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.partial_product_list_2t import PartialProductList2T


T = TypeVar("T", bound="JobStatusRT")


@_attrs_define
class JobStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'error-message': 'parameter out of range',
            'finished-at': '1996-12-19T16:39:57-08:00', 'id': 'urn:ivcap:job:123e4567-e89b-12d3-a456-426614174000', 'links':
            [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'name': 'Fire risk for Lot2', 'order':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'products': {'items': [{'data-href':
            'https:/.../1/artifacts/0000-00001220/blob', 'href': 'https:/.../1/artifacts/0000-00001220', 'mime-type':
            'image/geo+tiff', 'name': 'fire risk map', 'size': 1234963}], 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'next'}]}, 'request-content': 'Consequuntur tempora illum vel odio.', 'request-content-type':
            'application/json', 'requested-at': '1996-12-19T16:39:57-08:00', 'result-content': 'Iusto quis ut ipsum fugit.',
            'result-content-type': 'application/json', 'service': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000',
            'started-at': '1996-12-19T16:39:57-08:00', 'status': 'executing', 'tags': ['tag1', 'tag2']}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        id (str): ID Example: urn:ivcap:job:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        order (str): Reference to order Example: urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        policy (str): Reference to policy used Example: urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        request_content_type (str): Mime type of request Example: application/json.
        requested_at (datetime.datetime): DateTime job was submitted Example: 1996-12-19T16:39:57-08:00.
        service (str): Reference to service requested Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        status (JobStatusRTStatus): Job status Example: scheduled.
        error_message (Union[Unset, str]): Additional error message id status is 'Error' or 'Failed' Example: parameter
            out of range.
        finished_at (Union[Unset, datetime.datetime]): DateTime job processing finished Example:
            1996-12-19T16:39:57-08:00.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        products (Union[Unset, PartialProductList2T]):  Example: {'items': [{'data-href':
            'https:/.../1/artifacts/0000-00001220/blob', 'href': 'https:/.../1/artifacts/0000-00001220', 'mime-type':
            'image/geo+tiff', 'name': 'fire risk map', 'size': 1234963}], 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'next'}]}.
        request_content (Union[Unset, File]): Request content Example: Dolor nostrum eveniet..
        result_content (Union[Unset, File]): Result content Example: Eius similique..
        result_content_type (Union[Unset, str]): Mime type of result Example: application/json.
        started_at (Union[Unset, datetime.datetime]): DateTime job processing started Example:
            1996-12-19T16:39:57-08:00.
        tags (Union[Unset, list[str]]): Optional customer provided tags Example: ['tag1', 'tag2'].
    """

    account: str
    id: str
    links: list["LinkT"]
    order: str
    policy: str
    request_content_type: str
    requested_at: datetime.datetime
    service: str
    status: JobStatusRTStatus
    error_message: Union[Unset, str] = UNSET
    finished_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    products: Union[Unset, "PartialProductList2T"] = UNSET
    request_content: Union[Unset, Any] = UNSET
    result_content: Union[Unset, Any] = UNSET
    result_content_type: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        order = self.order

        policy = self.policy

        request_content_type = self.request_content_type

        requested_at = self.requested_at.isoformat()

        service = self.service

        status = self.status.value

        error_message = self.error_message

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        name = self.name

        products: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.products, Unset):
            products = self.products.to_dict()

        request_content: Union[Unset, Any] = UNSET
        if not isinstance(self.request_content, Unset):
            request_content = self.request_content

        result_content: Union[Unset, Any] = UNSET
        if not isinstance(self.result_content, Unset):
            result_content = self.result_content

        result_content_type = self.result_content_type

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "id": id,
                "links": links,
                "order": order,
                "policy": policy,
                "request-content-type": request_content_type,
                "requested-at": requested_at,
                "service": service,
                "status": status,
            }
        )
        if error_message is not UNSET:
            field_dict["error-message"] = error_message
        if finished_at is not UNSET:
            field_dict["finished-at"] = finished_at
        if name is not UNSET:
            field_dict["name"] = name
        if products is not UNSET:
            field_dict["products"] = products
        if request_content is not UNSET:
            field_dict["request-content"] = request_content
        if result_content is not UNSET:
            field_dict["result-content"] = result_content
        if result_content_type is not UNSET:
            field_dict["result-content-type"] = result_content_type
        if started_at is not UNSET:
            field_dict["started-at"] = started_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.partial_product_list_2t import PartialProductList2T

        d = src_dict.copy()
        account = d.pop("account")

        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        order = d.pop("order")

        policy = d.pop("policy")

        request_content_type = d.pop("request-content-type")

        requested_at = isoparse(d.pop("requested-at"))

        service = d.pop("service")

        status = JobStatusRTStatus(d.pop("status"))

        error_message = d.pop("error-message", UNSET)

        _finished_at = d.pop("finished-at", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        name = d.pop("name", UNSET)

        _products = d.pop("products", UNSET)
        products: Union[Unset, PartialProductList2T]
        if isinstance(_products, Unset):
            products = UNSET
        else:
            products = PartialProductList2T.from_dict(_products)

        _request_content = d.pop("request-content", UNSET)
        request_content: Union[Unset, Any]
        if isinstance(_request_content, Unset):
            request_content = UNSET
        else:
            request_content = _request_content

        _result_content = d.pop("result-content", UNSET)
        result_content: Union[Unset, Any]
        if isinstance(_result_content, Unset):
            result_content = UNSET
        else:
            result_content = _result_content

        result_content_type = d.pop("result-content-type", UNSET)

        _started_at = d.pop("started-at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        tags = cast(list[str], d.pop("tags", UNSET))

        job_status_rt = cls(
            account=account,
            id=id,
            links=links,
            order=order,
            policy=policy,
            request_content_type=request_content_type,
            requested_at=requested_at,
            service=service,
            status=status,
            error_message=error_message,
            finished_at=finished_at,
            name=name,
            products=products,
            request_content=request_content,
            result_content=result_content,
            result_content_type=result_content_type,
            started_at=started_at,
            tags=tags,
        )

        job_status_rt.additional_properties = d
        return job_status_rt

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
