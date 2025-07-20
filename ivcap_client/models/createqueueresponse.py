from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Createqueueresponse")


@_attrs_define
class Createqueueresponse:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'description': 'Events for the event
            service', 'id': 'urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000', 'name': 'events'}

    Attributes:
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        name (str): Name of the created queue. Example: events.
        account (Union[Unset, str]): Reference to billable account Example:
            urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        description (Union[Unset, str]): Description of the created queue. Example: Events for the event service.
    """

    id: str
    name: str
    account: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        account = self.account

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        account = d.pop("account", UNSET)

        description = d.pop("description", UNSET)

        createqueueresponse = cls(
            id=id,
            name=name,
            account=account,
            description=description,
        )

        createqueueresponse.additional_properties = d
        return createqueueresponse

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
