import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_status_rt_status import ProjectStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_properties import ProjectProperties


T = TypeVar("T", bound="ProjectStatusRT")


@_attrs_define
class ProjectStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d', 'created_at': '2023-03-17T04:57:00Z',
            'modified_at': '2023-03-17T04:57:00Z', 'name': 'My project name', 'parent':
            'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1', 'properties': {'details': 'Created for to investigate
            [objective]'}, 'status': 'unknown', 'urn': 'urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1'}

    Attributes:
        urn (str): Project URN Example: urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
        account (Union[Unset, str]): Account URN Example: urn:ivcap:account:146d4ac9-244a-4aee-aa32-a28f4b91e60d.
        created_at (Union[Unset, datetime.datetime]): DateTime project was created Example: 2023-03-17T04:57:00Z.
        modified_at (Union[Unset, datetime.datetime]): DateTime project last modified Example: 2023-03-17T04:57:00Z.
        name (Union[Unset, str]): Project name Example: My project name.
        parent (Union[Unset, str]): Parent Project URN Example: urn:ivcap:project:8a82775b-27d9-4635-b006-7ef5553656d1.
        properties (Union[Unset, ProjectProperties]):  Example: {'details': 'Created for to investigate [objective]'}.
        status (Union[Unset, ProjectStatusRTStatus]): Project status Example: deleted.
    """

    urn: str
    account: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    parent: Union[Unset, str] = UNSET
    properties: Union[Unset, "ProjectProperties"] = UNSET
    status: Union[Unset, ProjectStatusRTStatus] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        urn = self.urn

        account = self.account

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name

        parent = self.parent

        properties: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "urn": urn,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if modified_at is not UNSET:
            field_dict["modified_at"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if parent is not UNSET:
            field_dict["parent"] = parent
        if properties is not UNSET:
            field_dict["properties"] = properties
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.project_properties import ProjectProperties

        d = src_dict.copy()
        urn = d.pop("urn")

        account = d.pop("account", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _modified_at = d.pop("modified_at", UNSET)
        modified_at: Union[Unset, datetime.datetime]
        if isinstance(_modified_at, Unset):
            modified_at = UNSET
        else:
            modified_at = isoparse(_modified_at)

        name = d.pop("name", UNSET)

        parent = d.pop("parent", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ProjectProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ProjectProperties.from_dict(_properties)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ProjectStatusRTStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ProjectStatusRTStatus(_status)

        project_status_rt = cls(
            urn=urn,
            account=account,
            created_at=created_at,
            modified_at=modified_at,
            name=name,
            parent=parent,
            properties=properties,
            status=status,
        )

        project_status_rt.additional_properties = d
        return project_status_rt

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
