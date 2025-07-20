from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserListItem")


@_attrs_define
class UserListItem:
    """
    Example:
        {'email': 'example@domain.com', 'role': 'Owner', 'urn': 'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}

    Attributes:
        email (Union[Unset, str]): Email Example: example@domain.com.
        role (Union[Unset, str]): Role Example: Owner.
        urn (Union[Unset, str]): User URN Example: urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6.
    """

    email: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    urn: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role = self.role

        urn = self.urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if role is not UNSET:
            field_dict["role"] = role
        if urn is not UNSET:
            field_dict["urn"] = urn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        role = d.pop("role", UNSET)

        urn = d.pop("urn", UNSET)

        user_list_item = cls(
            email=email,
            role=role,
            urn=urn,
        )

        user_list_item.additional_properties = d
        return user_list_item

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
