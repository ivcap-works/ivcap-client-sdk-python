import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.nav_t import NavT
    from ..models.order_list_item import OrderListItem


T = TypeVar("T", bound="OrderListRT")


@attr.s(auto_attribs=True)
class OrderListRT:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'links': {'first': 'https://api.com/foo/...', 'next':
            'https://api.com/foo/...', 'self': 'https://api.com/foo/...'}, 'orders': [{'account_id': '2022-01-01',
            'finished_at': '2022-01-01', 'id': 'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis
            incidunt.'}, 'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}]}

    Attributes:
        at_time (datetime.datetime): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        links (NavT):  Example: {'first': 'https://api.com/foo/...', 'next': 'https://api.com/foo/...', 'self':
            'https://api.com/foo/...'}.
        orders (List['OrderListItem']): Orders Example: [{'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}, {'account_id': '2022-01-01', 'finished_at': '2022-01-01', 'id':
            'cayp:order:123e4567-e89b-12d3-a456-426614174000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis incidunt.'},
            'name': 'Fire risk for Lot2', 'ordered_at': '2022-01-01', 'service_id': '2022-01-01', 'started_at':
            '2022-01-01', 'status': 'finished'}].
    """

    at_time: datetime.datetime
    links: "NavT"
    orders: List["OrderListItem"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        at_time = self.at_time.isoformat()

        links = self.links.to_dict()

        orders = []
        for orders_item_data in self.orders:
            orders_item = orders_item_data.to_dict()

            orders.append(orders_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at-time": at_time,
                "links": links,
                "orders": orders,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.nav_t import NavT
        from ..models.order_list_item import OrderListItem

        d = src_dict.copy()
        at_time = isoparse(d.pop("at-time"))

        links = NavT.from_dict(d.pop("links"))

        orders = []
        _orders = d.pop("orders")
        for orders_item_data in _orders:
            orders_item = OrderListItem.from_dict(orders_item_data)

            orders.append(orders_item)

        order_list_rt = cls(
            at_time=at_time,
            links=links,
            orders=orders,
        )

        order_list_rt.additional_properties = d
        return order_list_rt

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
