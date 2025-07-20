from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PushResponseBody")


@_attrs_define
class PushResponseBody:
    """
    Example:
        {'digest': 'Omnis ipsam animi tempore.', 'exists': True}

    Attributes:
        digest (str): uploaded image digest or tag Example: Rerum nulla est vel reiciendis facere inventore..
        exists (bool): layer exists or not Example: True.
    """

    digest: str
    exists: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        digest = self.digest

        exists = self.exists

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "digest": digest,
                "exists": exists,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        digest = d.pop("digest")

        exists = d.pop("exists")

        push_response_body = cls(
            digest=digest,
            exists=exists,
        )

        push_response_body.additional_properties = d
        return push_response_body

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
