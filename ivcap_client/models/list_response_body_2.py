from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.secret_list_item import SecretListItem


T = TypeVar("T", bound="ListResponseBody2")


@_attrs_define
class ListResponseBody2:
    """
    Example:
        {'items': [{'expiry-time': 4932954319159294728, 'secret-name': 'Sint suscipit atque exercitationem nobis
            perspiciatis voluptate.'}, {'expiry-time': 4932954319159294728, 'secret-name': 'Sint suscipit atque
            exercitationem nobis perspiciatis voluptate.'}, {'expiry-time': 4932954319159294728, 'secret-name': 'Sint
            suscipit atque exercitationem nobis perspiciatis voluptate.'}], 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}]}

    Attributes:
        items (list['SecretListItem']): secrets Example: [{'expiry-time': 4932954319159294728, 'secret-name': 'Sint
            suscipit atque exercitationem nobis perspiciatis voluptate.'}, {'expiry-time': 4932954319159294728, 'secret-
            name': 'Sint suscipit atque exercitationem nobis perspiciatis voluptate.'}, {'expiry-time': 4932954319159294728,
            'secret-name': 'Sint suscipit atque exercitationem nobis perspiciatis voluptate.'}].
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}].
    """

    items: list["SecretListItem"]
    links: list["LinkT"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.secret_list_item import SecretListItem

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SecretListItem.from_dict(items_item_data)

            items.append(items_item)

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        list_response_body_2 = cls(
            items=items,
            links=links,
        )

        list_response_body_2.additional_properties = d
        return list_response_body_2

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
