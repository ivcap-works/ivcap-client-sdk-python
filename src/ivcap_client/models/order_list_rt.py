import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.order_list_item import OrderListItem


T = TypeVar("T", bound="OrderListRT")


@_attrs_define
class OrderListRT:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'items': [{'account':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name':
            'Fire risk for Lot2', 'ordered-at': '1996-12-19T16:39:57-08:00', 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at': '1996-12-19T16:39:57-08:00', 'status':
            'executing'}, {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2', 'ordered-at':
            '1996-12-19T16:39:57-08:00', 'service': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at':
            '1996-12-19T16:39:57-08:00', 'status': 'executing'}], 'links': [{'href': 'https://api.ivcap.net/1/....', 'rel':
            'self', 'type': 'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}]}

    Attributes:
        at_time (datetime.datetime): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        items (List['OrderListItem']): Orders Example: [{'account':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name':
            'Fire risk for Lot2', 'ordered-at': '1996-12-19T16:39:57-08:00', 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at': '1996-12-19T16:39:57-08:00', 'status':
            'executing'}, {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2', 'ordered-at':
            '1996-12-19T16:39:57-08:00', 'service': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at':
            '1996-12-19T16:39:57-08:00', 'status': 'executing'}, {'account':
            'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name':
            'Fire risk for Lot2', 'ordered-at': '1996-12-19T16:39:57-08:00', 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at': '1996-12-19T16:39:57-08:00', 'status':
            'executing'}, {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2', 'ordered-at':
            '1996-12-19T16:39:57-08:00', 'service': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at':
            '1996-12-19T16:39:57-08:00', 'status': 'executing'}].
        links (List['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}].
    """

    at_time: datetime.datetime
    items: List["OrderListItem"]
    links: List["LinkT"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        at_time = self.at_time.isoformat()

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at-time": at_time,
                "items": items,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.order_list_item import OrderListItem

        d = src_dict.copy()
        at_time = isoparse(d.pop("at-time"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = OrderListItem.from_dict(items_item_data)

            items.append(items_item)

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        order_list_rt = cls(
            at_time=at_time,
            items=items,
            links=links,
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
