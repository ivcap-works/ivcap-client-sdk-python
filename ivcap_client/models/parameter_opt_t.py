from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParameterOptT")


@_attrs_define
class ParameterOptT:
    """
    Example:
        {'description': 'Voluptate explicabo blanditiis eum.', 'value': 'Quidem velit et eveniet.'}

    Attributes:
        description (Union[Unset, str]):  Example: Quasi quia ducimus culpa..
        value (Union[Unset, str]):  Example: Rem eius nulla similique officiis..
    """

    description: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        value = d.pop("value", UNSET)

        parameter_opt_t = cls(
            description=description,
            value=value,
        )

        parameter_opt_t.additional_properties = d
        return parameter_opt_t

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
