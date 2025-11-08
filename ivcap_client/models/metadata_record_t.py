from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MetadataRecordT")


@_attrs_define
class MetadataRecordT:
    """
    Example:
        {'aspect': '{...}', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image'}

    Attributes:
        aspect (Any): Attached metadata aspect Example: {...}.
        entity (str): Entity ID Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000.
        schema (str): Schema ID Example: urn:blue:schema.image.
    """

    aspect: Any
    entity: str
    id: str
    schema: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aspect = self.aspect

        entity = self.entity

        id = self.id

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aspect": aspect,
                "entity": entity,
                "id": id,
                "schema": schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        aspect = d.pop("aspect")

        entity = d.pop("entity")

        id = d.pop("id")

        schema = d.pop("schema")

        metadata_record_t = cls(
            aspect=aspect,
            entity=entity,
            id=id,
            schema=schema,
        )

        metadata_record_t.additional_properties = d
        return metadata_record_t

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
