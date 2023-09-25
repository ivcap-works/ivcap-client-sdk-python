from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define, field

from ..models.order_status_rt_status import OrderStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_t import ParameterT
    from ..models.product_t import ProductT
    from ..models.ref_t import RefT
    from ..models.self_t import SelfT


T = TypeVar("T", bound="OrderStatusRT")


@define
class OrderStatusRT:
    """
    Example:
        {'account': {'id': 'http://beahan.net/laurie', 'links': {'describedBy': {'href': 'https://api.com/swagger/...',
            'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}, 'finished-at': '2023-03-17T04:57:00Z', 'id':
            '123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'name': 'Fire risk for Lot2', 'ordered-at':
            '2023-03-17T04:57:00Z', 'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold',
            'value': '10'}], 'products': [{'href': 'https:/.../1/artifacts/0000-00001220', 'mime-type': 'image/geo+tiff',
            'name': 'fire risk map', 'size': 1234963}], 'service': {'id': 'http://beahan.net/laurie', 'links':
            {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum
            odit.'}}, 'started-at': '2023-03-17T04:57:00Z', 'status': 'error', 'tags': ['tag1', 'tag2']}

    Attributes:
        id (str): Order ID Example: 123e4567-e89b-12d3-a456-426614174000.
        parameters (List['ParameterT']): Service parameters Example: [{'name': 'region', 'value': 'Upper Valley'},
            {'name': 'threshold', 'value': '10'}].
        account (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        finished_at (Union[Unset, str]): DateTime order processing finished Example: 2023-03-17T04:57:00Z.
        links (Union[Unset, SelfT]):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'At qui.'}.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        ordered_at (Union[Unset, str]): DateTime order was placed Example: 2023-03-17T04:57:00Z.
        products (Union[Unset, List['ProductT']]): Products delivered for this order Example: [{'href':
            'https:/.../1/artifacts/0000-00001220', 'mime-type': 'image/geo+tiff', 'name': 'fire risk map', 'size':
            1234963}].
        service (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        started_at (Union[Unset, str]): DateTime order processing started Example: 2023-03-17T04:57:00Z.
        status (Union[Unset, OrderStatusRTStatus]): Order status Example: scheduled.
        tags (Union[Unset, List[str]]): Optional customer provided tags Example: ['tag1', 'tag2'].
    """

    id: str
    parameters: List["ParameterT"]
    account: Union[Unset, "RefT"] = UNSET
    finished_at: Union[Unset, str] = UNSET
    links: Union[Unset, "SelfT"] = UNSET
    name: Union[Unset, str] = UNSET
    ordered_at: Union[Unset, str] = UNSET
    products: Union[Unset, List["ProductT"]] = UNSET
    service: Union[Unset, "RefT"] = UNSET
    started_at: Union[Unset, str] = UNSET
    status: Union[Unset, OrderStatusRTStatus] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()

            parameters.append(parameters_item)

        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        finished_at = self.finished_at
        links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        name = self.name
        ordered_at = self.ordered_at
        products: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.products, Unset):
            products = []
            for products_item_data in self.products:
                products_item = products_item_data.to_dict()

                products.append(products_item)

        service: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.service, Unset):
            service = self.service.to_dict()

        started_at = self.started_at
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "parameters": parameters,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if finished_at is not UNSET:
            field_dict["finished-at"] = finished_at
        if links is not UNSET:
            field_dict["links"] = links
        if name is not UNSET:
            field_dict["name"] = name
        if ordered_at is not UNSET:
            field_dict["ordered-at"] = ordered_at
        if products is not UNSET:
            field_dict["products"] = products
        if service is not UNSET:
            field_dict["service"] = service
        if started_at is not UNSET:
            field_dict["started-at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_t import ParameterT
        from ..models.product_t import ProductT
        from ..models.ref_t import RefT
        from ..models.self_t import SelfT

        d = src_dict.copy()
        id = d.pop("id")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        _account = d.pop("account", UNSET)
        account: Union[Unset, RefT]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = RefT.from_dict(_account)

        finished_at = d.pop("finished-at", UNSET)

        _links = d.pop("links", UNSET)
        links: Union[Unset, SelfT]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = SelfT.from_dict(_links)

        name = d.pop("name", UNSET)

        ordered_at = d.pop("ordered-at", UNSET)

        products = []
        _products = d.pop("products", UNSET)
        for products_item_data in _products or []:
            products_item = ProductT.from_dict(products_item_data)

            products.append(products_item)

        _service = d.pop("service", UNSET)
        service: Union[Unset, RefT]
        if isinstance(_service, Unset):
            service = UNSET
        else:
            service = RefT.from_dict(_service)

        started_at = d.pop("started-at", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, OrderStatusRTStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = OrderStatusRTStatus(_status)

        tags = cast(List[str], d.pop("tags", UNSET))

        order_status_rt = cls(
            id=id,
            parameters=parameters,
            account=account,
            finished_at=finished_at,
            links=links,
            name=name,
            ordered_at=ordered_at,
            products=products,
            service=service,
            started_at=started_at,
            status=status,
            tags=tags,
        )

        order_status_rt.additional_properties = d
        return order_status_rt

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
