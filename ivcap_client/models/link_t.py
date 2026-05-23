from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LinkT")


@_attrs_define
class LinkT:
    """
    Example:
        {'href': 'https://acme.com/..', 'rel': 'self, describedBy, next, first', 'type': 'application/json'}

    Attributes:
        href (str): web link Example: https://acme.com/...
        rel (str): relation type Example: self, describedBy, next, first.
        type_ (str): mime type Example: application/json.
    """

    href: str
    rel: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        rel = self.rel

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "href": href,
                "rel": rel,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        href = d.pop("href")

        rel = d.pop("rel")

        type_ = d.pop("type")

        link_t = cls(
            href=href,
            rel=rel,
            type_=type_,
        )

        link_t.additional_properties = d
        return link_t

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
