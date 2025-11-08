from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectBase")


@_attrs_define
class ProjectBase:
    """
    Example:
        {'name': 'My project name', 'urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1'}

    Attributes:
        name (Union[Unset, str]): Project name Example: My project name.
        urn (Union[Unset, str]): Project URN Example: urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
    """

    name: Union[Unset, str] = UNSET
    urn: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        urn = self.urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if urn is not UNSET:
            field_dict["urn"] = urn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        urn = d.pop("urn", UNSET)

        project_base = cls(
            name=name,
            urn=urn,
        )

        project_base.additional_properties = d
        return project_base

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
