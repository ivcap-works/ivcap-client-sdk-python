from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TemporaryRedirectT")


@_attrs_define
class TemporaryRedirectT:
    """Temporarily redirecting to a different URL

    Example:
        {'location': 'Asperiores aut accusantium.'}

    Attributes:
        location (str): the URL for the job Example: At dolorem dolores ut sint dolorum qui..
    """

    location: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location = self.location

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location": location,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        location = d.pop("location")

        temporary_redirect_t = cls(
            location=location,
        )

        temporary_redirect_t.additional_properties = d
        return temporary_redirect_t

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
