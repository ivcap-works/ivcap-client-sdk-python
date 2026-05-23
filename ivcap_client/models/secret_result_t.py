from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecretResultT")


@_attrs_define
class SecretResultT:
    """
    Example:
        {'expiry-time': 5171408676313242593, 'secret-name': 'Nostrum quibusdam quia aut.', 'secret-value': 'Sapiente
            commodi dolorem.'}

    Attributes:
        expiry_time (int): Expiry time Example: 3916875198971840530.
        secret_name (str): Secret name Example: Id et cupiditate tenetur ratione qui amet..
        secret_value (str): Secret value Example: Debitis perferendis..
    """

    expiry_time: int
    secret_name: str
    secret_value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiry_time = self.expiry_time

        secret_name = self.secret_name

        secret_value = self.secret_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expiry-time": expiry_time,
                "secret-name": secret_name,
                "secret-value": secret_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expiry_time = d.pop("expiry-time")

        secret_name = d.pop("secret-name")

        secret_value = d.pop("secret-value")

        secret_result_t = cls(
            expiry_time=expiry_time,
            secret_name=secret_name,
            secret_value=secret_value,
        )

        secret_result_t.additional_properties = d
        return secret_result_t

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
