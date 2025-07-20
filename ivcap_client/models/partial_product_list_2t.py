from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.product_list_item_2t import ProductListItem2T


T = TypeVar("T", bound="PartialProductList2T")


@_attrs_define
class PartialProductList2T:
    """
    Example:
        {'items': [{'data-href': 'https:/.../1/artifacts/0000-00001220/blob', 'href':
            'https:/.../1/artifacts/0000-00001220', 'mime-type': 'image/geo+tiff', 'name': 'fire risk map', 'size':
            1234963}], 'links': [{'href': 'https://api.ivcap.net/1/....', 'rel': 'next'}]}

    Attributes:
        items (list['ProductListItem2T']): (Partial) list of products delivered by this order Example: [{'data-href':
            'https:/.../1/artifacts/0000-00001220/blob', 'href': 'https:/.../1/artifacts/0000-00001220', 'mime-type':
            'image/geo+tiff', 'name': 'fire risk map', 'size': 1234963}].
        links (list['LinkT']): Links to more products, if there are any Example: [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'next'}].
    """

    items: list["ProductListItem2T"]
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
        from ..models.product_list_item_2t import ProductListItem2T

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ProductListItem2T.from_dict(items_item_data)

            items.append(items_item)

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        partial_product_list_2t = cls(
            items=items,
            links=links,
        )

        partial_product_list_2t.additional_properties = d
        return partial_product_list_2t

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
