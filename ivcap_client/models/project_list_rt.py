import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_list_item import ProjectListItem


T = TypeVar("T", bound="ProjectListRT")


@_attrs_define
class ProjectListRT:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'page': 'Et quibusdam.', 'projects': [{'at-time':
            '1996-12-19T16:39:57-08:00', 'created_at': '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z',
            'name': 'MineralsCollection', 'role': 'Member', 'urn':
            'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}, {'at-time': '1996-12-19T16:39:57-08:00',
            'created_at': '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z', 'name': 'MineralsCollection',
            'role': 'Member', 'urn': 'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}, {'at-time':
            '1996-12-19T16:39:57-08:00', 'created_at': '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z',
            'name': 'MineralsCollection', 'role': 'Member', 'urn':
            'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}]}

    Attributes:
        projects (list['ProjectListItem']):  Example: [{'at-time': '1996-12-19T16:39:57-08:00', 'created_at':
            '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z', 'name': 'MineralsCollection', 'role': 'Member',
            'urn': 'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}, {'at-time': '1996-12-19T16:39:57-08:00',
            'created_at': '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z', 'name': 'MineralsCollection',
            'role': 'Member', 'urn': 'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}, {'at-time':
            '1996-12-19T16:39:57-08:00', 'created_at': '2023-03-17T04:57:00Z', 'modified_at': '2023-03-17T04:57:00Z',
            'name': 'MineralsCollection', 'role': 'Member', 'urn':
            'urn:ivcap:project:53cbb715-4ffd-4158-9e55-5d0ae69605a4'}].
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        page (Union[Unset, str]): A pagination token to retrieve the next set of results. Empty if there are no more
            results Example: Est reiciendis enim..
    """

    projects: list["ProjectListItem"]
    at_time: Union[Unset, datetime.datetime] = UNSET
    page: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        projects = []
        for componentsschemas_project_list_item_collection_item_data in self.projects:
            componentsschemas_project_list_item_collection_item = (
                componentsschemas_project_list_item_collection_item_data.to_dict()
            )
            projects.append(componentsschemas_project_list_item_collection_item)

        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        page = self.page

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "projects": projects,
            }
        )
        if at_time is not UNSET:
            field_dict["at-time"] = at_time
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.project_list_item import ProjectListItem

        d = src_dict.copy()
        projects = []
        _projects = d.pop("projects")
        for componentsschemas_project_list_item_collection_item_data in _projects:
            componentsschemas_project_list_item_collection_item = ProjectListItem.from_dict(
                componentsschemas_project_list_item_collection_item_data
            )

            projects.append(componentsschemas_project_list_item_collection_item)

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        page = d.pop("page", UNSET)

        project_list_rt = cls(
            projects=projects,
            at_time=at_time,
            page=page,
        )

        project_list_rt.additional_properties = d
        return project_list_rt

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
