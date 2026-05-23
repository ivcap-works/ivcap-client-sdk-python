from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetProjectAccountRequestBody")


@_attrs_define
class SetProjectAccountRequestBody:
    """
    Example:
        {'account_urn': 'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d'}

    Attributes:
        account_urn (str): Account URN Example: urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d.
    """

    account_urn: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account_urn = self.account_urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account_urn": account_urn,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        account_urn = d.pop("account_urn")

        set_project_account_request_body = cls(
            account_urn=account_urn,
        )

        set_project_account_request_body.additional_properties = d
        return set_project_account_request_body

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
