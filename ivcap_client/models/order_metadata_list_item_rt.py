from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrderMetadataListItemRT")


@_attrs_define
class OrderMetadataListItemRT:
    """
    Example:
        {'content-type': '{...}', 'href': '{...}', 'id': 'urn:ivcap:aspect ID:123e4567-e89b-12d3-a456-426614174000',
            'schema': 'urn:blue:schema.image'}

    Attributes:
        content_type (str): type of metadata content Example: {...}.
        href (str): reference to content of metadata Example: {...}.
        id (str): ID Example: urn:ivcap:aspect ID:123e4567-e89b-12d3-a456-426614174000.
        schema (str): Schema ID Example: urn:blue:schema.image.
    """

    content_type: str
    href: str
    id: str
    schema: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        href = self.href

        id = self.id

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content-type": content_type,
                "href": href,
                "id": id,
                "schema": schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        content_type = d.pop("content-type")

        href = d.pop("href")

        id = d.pop("id")

        schema = d.pop("schema")

        order_metadata_list_item_rt = cls(
            content_type=content_type,
            href=href,
            id=id,
            schema=schema,
        )

        order_metadata_list_item_rt.additional_properties = d
        return order_metadata_list_item_rt

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
