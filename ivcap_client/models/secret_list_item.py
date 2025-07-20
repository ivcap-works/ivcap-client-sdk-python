from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecretListItem")


@_attrs_define
class SecretListItem:
    """
    Example:
        {'expiry-time': 802817397779052927, 'secret-name': 'Commodi dolorem provident ab et.'}

    Attributes:
        expiry_time (int): Expiry time Example: 4099636861052818756.
        secret_name (str): Secret name Example: Dolor quas sed magni aliquam in voluptatem..
    """

    expiry_time: int
    secret_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiry_time = self.expiry_time

        secret_name = self.secret_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expiry-time": expiry_time,
                "secret-name": secret_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expiry_time = d.pop("expiry-time")

        secret_name = d.pop("secret-name")

        secret_list_item = cls(
            expiry_time=expiry_time,
            secret_name=secret_name,
        )

        secret_list_item.additional_properties = d
        return secret_list_item

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
