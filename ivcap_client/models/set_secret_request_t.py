from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetSecretRequestT")


@_attrs_define
class SetSecretRequestT:
    """
    Example:
        {'expiry-time': 3640280021039679283, 'secret-name': 'Magni reprehenderit reprehenderit ratione accusamus.',
            'secret-type': 'Iusto iste iusto quisquam consequatur voluptas eius.', 'secret-value': 'Error id et.'}

    Attributes:
        expiry_time (int): Expiry time Example: 2773099974567600988.
        secret_name (str): Secret name Example: Numquam adipisci..
        secret_value (str): Secret value Example: Commodi beatae commodi..
        secret_type (Union[Unset, str]): Secret type Example: Aut officia et iure..
    """

    expiry_time: int
    secret_name: str
    secret_value: str
    secret_type: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expiry_time = self.expiry_time

        secret_name = self.secret_name

        secret_value = self.secret_value

        secret_type = self.secret_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expiry-time": expiry_time,
                "secret-name": secret_name,
                "secret-value": secret_value,
            }
        )
        if secret_type is not UNSET:
            field_dict["secret-type"] = secret_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expiry_time = d.pop("expiry-time")

        secret_name = d.pop("secret-name")

        secret_value = d.pop("secret-value")

        secret_type = d.pop("secret-type", UNSET)

        set_secret_request_t = cls(
            expiry_time=expiry_time,
            secret_name=secret_name,
            secret_value=secret_value,
            secret_type=secret_type,
        )

        set_secret_request_t.additional_properties = d
        return set_secret_request_t

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
