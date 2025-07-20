import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.order_status_rt_status import OrderStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.parameter_t import ParameterT
    from ..models.partial_product_list_2t import PartialProductList2T


T = TypeVar("T", bound="OrderStatusRT")


@_attrs_define
class OrderStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at':
            '1996-12-19T16:39:57-08:00', 'id': 'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'name': 'Fire risk for Lot2', 'ordered-at': '1996-12-19T16:39:57-08:00', 'parameters':
            [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value': '10'}], 'products': {'items':
            [{'data-href': 'https:/.../1/artifacts/0000-00001220/blob', 'href': 'https:/.../1/artifacts/0000-00001220',
            'mime-type': 'image/geo+tiff', 'name': 'fire risk map', 'size': 1234963}], 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'next'}]}, 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at': '1996-12-19T16:39:57-08:00', 'status':
            'failed', 'tags': ['tag1', 'tag2']}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        id (str): ID Example: urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        parameters (list['ParameterT']): Service parameters Example: [{'name': 'region', 'value': 'Upper Valley'},
            {'name': 'threshold', 'value': '10'}].
        products (PartialProductList2T):  Example: {'items': [{'data-href': 'https:/.../1/artifacts/0000-00001220/blob',
            'href': 'https:/.../1/artifacts/0000-00001220', 'mime-type': 'image/geo+tiff', 'name': 'fire risk map', 'size':
            1234963}], 'links': [{'href': 'https://api.ivcap.net/1/....', 'rel': 'next'}]}.
        service (str): Reference to service requested Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        status (OrderStatusRTStatus): Order status Example: failed.
        finished_at (Union[Unset, datetime.datetime]): DateTime order processing finished Example:
            1996-12-19T16:39:57-08:00.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        ordered_at (Union[Unset, datetime.datetime]): DateTime order was placed Example: 1996-12-19T16:39:57-08:00.
        started_at (Union[Unset, datetime.datetime]): DateTime order processing started Example:
            1996-12-19T16:39:57-08:00.
        tags (Union[Unset, list[str]]): Optional customer provided tags Example: ['tag1', 'tag2'].
    """

    account: str
    id: str
    links: list["LinkT"]
    parameters: list["ParameterT"]
    products: "PartialProductList2T"
    service: str
    status: OrderStatusRTStatus
    finished_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    ordered_at: Union[Unset, datetime.datetime] = UNSET
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

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        products = self.products.to_dict()

        service = self.service

        status = self.status.value

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        name = self.name

        ordered_at: Union[Unset, str] = UNSET
        if not isinstance(self.ordered_at, Unset):
            ordered_at = self.ordered_at.isoformat()

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
                "parameters": parameters,
                "products": products,
                "service": service,
                "status": status,
            }
        )
        if finished_at is not UNSET:
            field_dict["finished-at"] = finished_at
        if name is not UNSET:
            field_dict["name"] = name
        if ordered_at is not UNSET:
            field_dict["ordered-at"] = ordered_at
        if started_at is not UNSET:
            field_dict["started-at"] = started_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.parameter_t import ParameterT
        from ..models.partial_product_list_2t import PartialProductList2T

        d = src_dict.copy()
        account = d.pop("account")

        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        products = PartialProductList2T.from_dict(d.pop("products"))

        service = d.pop("service")

        status = OrderStatusRTStatus(d.pop("status"))

        _finished_at = d.pop("finished-at", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        name = d.pop("name", UNSET)

        _ordered_at = d.pop("ordered-at", UNSET)
        ordered_at: Union[Unset, datetime.datetime]
        if isinstance(_ordered_at, Unset):
            ordered_at = UNSET
        else:
            ordered_at = isoparse(_ordered_at)

        _started_at = d.pop("started-at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        tags = cast(list[str], d.pop("tags", UNSET))

        order_status_rt = cls(
            account=account,
            id=id,
            links=links,
            parameters=parameters,
            products=products,
            service=service,
            status=status,
            finished_at=finished_at,
            name=name,
            ordered_at=ordered_at,
            started_at=started_at,
            tags=tags,
        )

        order_status_rt.additional_properties = d
        return order_status_rt

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
