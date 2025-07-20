from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceNotFoundT")


@_attrs_define
class ResourceNotFoundT:
    """Resource not found

    Example:
        {'id': 'cayp:type:123e4567-e89b-12d3-a456-426614174000', 'message': 'Resource 123...00 not found'}

    Attributes:
        id (str): ID of missing resource Example: cayp:type:123e4567-e89b-12d3-a456-426614174000.
        message (str): Message of error Example: Resource 123...00 not found.
    """

    id: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        message = d.pop("message")

        resource_not_found_t = cls(
            id=id,
            message=message,
        )

        resource_not_found_t.additional_properties = d
        return resource_not_found_t

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
