import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Createqueueresponse")


@_attrs_define
class Createqueueresponse:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'created-at': '1996-12-19T16:39:57-08:00',
            'description': 'Events for the event service', 'id': 'urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000',
            'name': 'events'}

    Attributes:
        created_at (datetime.datetime): Timestamp when the queue was created Example: 1996-12-19T16:39:57-08:00.
        id (str): queue Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        name (str): Name of the created queue. Example: events.
        account (Union[Unset, str]): Reference to billable account Example:
            urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        description (Union[Unset, str]): Description of the created queue. Example: Events for the event service.
    """

    created_at: datetime.datetime
    id: str
    name: str
    account: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        name = self.name

        account = self.account

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created-at": created_at,
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created-at"))

        id = d.pop("id")

        name = d.pop("name")

        account = d.pop("account", UNSET)

        description = d.pop("description", UNSET)

        createqueueresponse = cls(
            created_at=created_at,
            id=id,
            name=name,
            account=account,
            description=description,
        )

        createqueueresponse.additional_properties = d
        return createqueueresponse

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
