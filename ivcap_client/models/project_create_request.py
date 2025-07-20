from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        {'account_urn': 'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'name': 'My project name',
            'parent_project_urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1', 'properties': {'details':
            'Created for to investigate [objective]'}}

    Attributes:
        name (str): Project name Example: My project name.
        account_urn (Union[Unset, str]): URN of the billing account Example: urn:ivcap:account:146d4ac9-244a-4aee-
            aa32-a28f4b91e60d.
        parent_project_urn (Union[Unset, str]): URN of the parent project Example:
            urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
        properties (Union[Unset, ProjectProperties]):  Example: {'details': 'Created for to investigate [objective]'}.
    """

    name: str
    account_urn: Union[Unset, str] = UNSET
    parent_project_urn: Union[Unset, str] = UNSET
    properties: Union[Unset, "ProjectProperties"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        account_urn = self.account_urn

        parent_project_urn = self.parent_project_urn

        properties: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if account_urn is not UNSET:
            field_dict["account_urn"] = account_urn
        if parent_project_urn is not UNSET:
            field_dict["parent_project_urn"] = parent_project_urn
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.project_properties import ProjectProperties

        d = src_dict.copy()
        name = d.pop("name")

        account_urn = d.pop("account_urn", UNSET)

        parent_project_urn = d.pop("parent_project_urn", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ProjectProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProjectProperties.from_dict(_properties)

        project_create_request = cls(
            name=name,
            account_urn=account_urn,
            parent_project_urn=parent_project_urn,
            properties=properties,
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
