from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AddMetaRT")


@_attrs_define
class AddMetaRT:
    """
    Example:
        {'record-id': 'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        record_id (str): Reference to record created Example: urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000.
    """

    record_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        record_id = self.record_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "record-id": record_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        record_id = d.pop("record-id")

        add_meta_rt = cls(
            record_id=record_id,
        )

        add_meta_rt.additional_properties = d
        return add_meta_rt

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
