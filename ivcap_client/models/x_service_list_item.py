import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="XServiceListItem")


@_attrs_define
class XServiceListItem:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'banner': 'urn:....', 'description': 'Some
            lengthy description of fire risk', 'href': 'https://api.ivcap.net/1/services/...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for region', 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'published-at': '1996-12-19T16:39:57-08:00'}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        href (str):  Example: https://api.ivcap.net/1/services/....
        id (str): ID Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        banner (Union[Unset, str]): Optional banner image for this service Example: urn:.....
        description (Union[Unset, str]): Optional description of the service Example: Some lengthy description of fire
            risk.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for region.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        published_at (Union[Unset, datetime.datetime]): time this service was published Example:
            1996-12-19T16:39:57-08:00.
    """

    account: str
    href: str
    id: str
    banner: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    published_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        href = self.href

        id = self.id

        banner = self.banner

        description = self.description

        name = self.name

        policy = self.policy

        published_at: Union[Unset, str] = UNSET
        if not isinstance(self.published_at, Unset):
            published_at = self.published_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "href": href,
                "id": id,
            }
        )
        if banner is not UNSET:
            field_dict["banner"] = banner
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if published_at is not UNSET:
            field_dict["published-at"] = published_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        account = d.pop("account")

        href = d.pop("href")

        id = d.pop("id")

        banner = d.pop("banner", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        _published_at = d.pop("published-at", UNSET)
        published_at: Union[Unset, datetime.datetime]
        if isinstance(_published_at, Unset):
            published_at = UNSET
        else:
            published_at = isoparse(_published_at)

        x_service_list_item = cls(
            account=account,
            href=href,
            id=id,
            banner=banner,
            description=description,
            name=name,
            policy=policy,
            published_at=published_at,
        )

        x_service_list_item.additional_properties = d
        return x_service_list_item

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
