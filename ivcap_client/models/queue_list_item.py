from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QueueListItem")


@_attrs_define
class QueueListItem:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'description': 'Events for the event
            service', 'href': 'https://api.ivcap.net/1/queues/...', 'id':
            'urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000', 'name': 'events'}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        href (str):  Example: https://api.ivcap.net/1/queues/....
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        description (Union[Unset, str]): Description of the created queue. Example: Events for the event service.
        name (Union[Unset, str]): Name of the created queue. Example: events.
    """

    account: str
    href: str
    id: str
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        href = self.href

        id = self.id

        description = self.description

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "href": href,
                "id": id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        account = d.pop("account")

        href = d.pop("href")

        id = d.pop("id")

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        queue_list_item = cls(
            account=account,
            href=href,
            id=id,
            description=description,
            name=name,
        )

        queue_list_item.additional_properties = d
        return queue_list_item

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
