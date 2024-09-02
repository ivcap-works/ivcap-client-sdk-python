from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.link_t import LinkT


T = TypeVar("T", bound="ListResponseBody")


@_attrs_define
class ListResponseBody:
    """
    Example:
        {'items': ['Consequuntur commodi beatae commodi optio.', 'Magni reprehenderit reprehenderit ratione accusamus.',
            'Iusto iste iusto quisquam consequatur voluptas eius.'], 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'self', 'type': 'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}]}

    Attributes:
        items (List[str]): docker image tags Example: ['Consequatur qui voluptatem.', 'Earum aliquid quia repellat
            ipsum.', 'Adipisci optio aut officia.'].
        links (List['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}].
    """

    items: List[str]
    links: List["LinkT"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items = self.items

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "links": links,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.link_t import LinkT

        d = src_dict.copy()
        items = cast(List[str], d.pop("items"))

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        list_response_body = cls(
            items=items,
            links=links,
        )

        list_response_body.additional_properties = d
        return list_response_body

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
