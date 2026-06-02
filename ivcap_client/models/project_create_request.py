from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_properties import ProjectProperties


T = TypeVar("T", bound="ProjectCreateRequest")


@_attrs_define
class ProjectCreateRequest:
    """
    Example:
        {'account': 'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name', 'parent':
            'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1', 'properties': {'details': 'Created to investigate
            [objective]'}, 'urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1'}

    Attributes:
        name (str): Project name Example: My project name.
        account (str | Unset): Account URN Example: urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d.
        parent (str | Unset): Parent Project URN Example: urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
        properties (ProjectProperties | Unset):  Example: {'details': 'Created to investigate [objective]'}.
        urn (str | Unset): Project URN Example: urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
    """

    name: str
    account: str | Unset = UNSET
    parent: str | Unset = UNSET
    properties: ProjectProperties | Unset = UNSET
    urn: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        account = self.account

        parent = self.parent

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        urn = self.urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if parent is not UNSET:
            field_dict["parent"] = parent
        if properties is not UNSET:
            field_dict["properties"] = properties
        if urn is not UNSET:
            field_dict["urn"] = urn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_properties import ProjectProperties

        d = dict(src_dict)
        name = d.pop("name")

        account = d.pop("account", UNSET)

        parent = d.pop("parent", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: ProjectProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProjectProperties.from_dict(_properties)

        urn = d.pop("urn", UNSET)

        project_create_request = cls(
            name=name,
            account=account,
            parent=parent,
            properties=properties,
            urn=urn,
        )

        project_create_request.additional_properties = d
        return project_create_request

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
