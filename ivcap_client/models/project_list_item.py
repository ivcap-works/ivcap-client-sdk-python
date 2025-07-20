import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectListItem")


@_attrs_define
class ProjectListItem:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'created_at': '2023-03-17T04:57:00Z', 'modified_at':
            '2023-03-17T04:57:00Z', 'name': 'MineralsCollection', 'role': 'Member', 'urn':
            'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}

    Attributes:
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        created_at (Union[Unset, datetime.datetime]): DateTime project was created Example: 2023-03-17T04:57:00Z.
        modified_at (Union[Unset, datetime.datetime]): DateTime project last modified Example: 2023-03-17T04:57:00Z.
        name (Union[Unset, str]): Project Name Example: MineralsCollection.
        role (Union[Unset, str]): User Role Example: Member.
        urn (Union[Unset, str]): Project URN Example: urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4.
    """

    at_time: Union[Unset, datetime.datetime] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    urn: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name

        role = self.role

        urn = self.urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if at_time is not UNSET:
            field_dict["at-time"] = at_time
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if modified_at is not UNSET:
            field_dict["modified_at"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role
        if urn is not UNSET:
            field_dict["urn"] = urn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

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

        role = d.pop("role", UNSET)

        urn = d.pop("urn", UNSET)

        project_list_item = cls(
            at_time=at_time,
            created_at=created_at,
            modified_at=modified_at,
            name=name,
            role=role,
            urn=urn,
        )

        project_list_item.additional_properties = d
        return project_list_item

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
