import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_list_item import UserListItem


T = TypeVar("T", bound="MembersList")


@_attrs_define
class MembersList:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'members': [{'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}, {'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}, {'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}, {'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}], 'page': 'Et inventore exercitationem blanditiis omnis
            magnam.'}

    Attributes:
        members (list['UserListItem']): Members Example: [{'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}, {'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}, {'email': 'example@domain.com', 'role': 'Owner', 'urn':
            'urn:ivcap:user:0190804b-a48c-758e-839b-8ee2ed25aec6'}].
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        page (Union[Unset, str]): A pagination token to retrieve the next set of results. Empty if there are no more
            results Example: Mollitia animi sapiente eos libero mollitia quis..
    """

    members: list["UserListItem"]
    at_time: Union[Unset, datetime.datetime] = UNSET
    page: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        members = []
        for members_item_data in self.members:
            members_item = members_item_data.to_dict()
            members.append(members_item)

        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        page = self.page

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "members": members,
            }
        )
        if at_time is not UNSET:
            field_dict["at-time"] = at_time
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_list_item import UserListItem

        d = src_dict.copy()
        members = []
        _members = d.pop("members")
        for members_item_data in _members:
            members_item = UserListItem.from_dict(members_item_data)

            members.append(members_item)

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        page = d.pop("page", UNSET)

        members_list = cls(
            members=members,
            at_time=at_time,
            page=page,
        )

        members_list.additional_properties = d
        return members_list

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
