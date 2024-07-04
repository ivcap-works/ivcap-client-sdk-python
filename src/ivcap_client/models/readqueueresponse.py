import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Readqueueresponse")


@_attrs_define
class Readqueueresponse:
    """
    Example:
        {'bytes': 1742645208466165557, 'consumer-count': 1253965597670358472, 'created-at': '1996-12-19T16:39:57-08:00',
            'description': 'Events for the event service', 'first-id': 'http://bins.biz/cordell_kovacek', 'first-time':
            '1996-12-19T16:39:57-08:00', 'id': 'urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000', 'last-id':
            'http://leannon.info/treva', 'last-time': '1996-12-19T16:39:57-08:00', 'name': 'events', 'total-messages':
            5765006188850863462}

    Attributes:
        created_at (datetime.datetime): Timestamp when the queue was created Example: 1996-12-19T16:39:57-08:00.
        id (str): ID Example: urn:ivcap:queue:123e4567-e89b-12d3-a456-426614174000.
        name (str): Name of the queue. Example: events.
        bytes_ (Union[Unset, int]): Number of bytes in the queue Example: 14261317834828336776.
        consumer_count (Union[Unset, int]): Number of consumers Example: 1004337198302308113.
        description (Union[Unset, str]): Description of the queue. Example: Events for the event service.
        first_id (Union[Unset, str]): First identifier in the queue Example: http://beatty.info/vida.
        first_time (Union[Unset, datetime.datetime]): Timestamp of the first message in the queue Example:
            1996-12-19T16:39:57-08:00.
        last_id (Union[Unset, str]): Last identifier in the queue Example: http://hodkiewicz.net/jordi.hansen.
        last_time (Union[Unset, datetime.datetime]): Timestamp of the last message in the queue Example:
            1996-12-19T16:39:57-08:00.
        total_messages (Union[Unset, int]): Number of messages sent to the queue Example: 6527866174719529844.
    """

    created_at: datetime.datetime
    id: str
    name: str
    bytes_: Union[Unset, int] = UNSET
    consumer_count: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    first_id: Union[Unset, str] = UNSET
    first_time: Union[Unset, datetime.datetime] = UNSET
    last_id: Union[Unset, str] = UNSET
    last_time: Union[Unset, datetime.datetime] = UNSET
    total_messages: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id

        name = self.name

        bytes_ = self.bytes_

        consumer_count = self.consumer_count

        description = self.description

        first_id = self.first_id

        first_time: Union[Unset, str] = UNSET
        if not isinstance(self.first_time, Unset):
            first_time = self.first_time.isoformat()

        last_id = self.last_id

        last_time: Union[Unset, str] = UNSET
        if not isinstance(self.last_time, Unset):
            last_time = self.last_time.isoformat()

        total_messages = self.total_messages

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created-at": created_at,
                "id": id,
                "name": name,
            }
        )
        if bytes_ is not UNSET:
            field_dict["bytes"] = bytes_
        if consumer_count is not UNSET:
            field_dict["consumer-count"] = consumer_count
        if description is not UNSET:
            field_dict["description"] = description
        if first_id is not UNSET:
            field_dict["first-id"] = first_id
        if first_time is not UNSET:
            field_dict["first-time"] = first_time
        if last_id is not UNSET:
            field_dict["last-id"] = last_id
        if last_time is not UNSET:
            field_dict["last-time"] = last_time
        if total_messages is not UNSET:
            field_dict["total-messages"] = total_messages

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created-at"))

        id = d.pop("id")

        name = d.pop("name")

        bytes_ = d.pop("bytes", UNSET)

        consumer_count = d.pop("consumer-count", UNSET)

        description = d.pop("description", UNSET)

        first_id = d.pop("first-id", UNSET)

        _first_time = d.pop("first-time", UNSET)
        first_time: Union[Unset, datetime.datetime]
        if isinstance(_first_time, Unset):
            first_time = UNSET
        else:
            first_time = isoparse(_first_time)

        last_id = d.pop("last-id", UNSET)

        _last_time = d.pop("last-time", UNSET)
        last_time: Union[Unset, datetime.datetime]
        if isinstance(_last_time, Unset):
            last_time = UNSET
        else:
            last_time = isoparse(_last_time)

        total_messages = d.pop("total-messages", UNSET)

        readqueueresponse = cls(
            created_at=created_at,
            id=id,
            name=name,
            bytes_=bytes_,
            consumer_count=consumer_count,
            description=description,
            first_id=first_id,
            first_time=first_time,
            last_id=last_id,
            last_time=last_time,
            total_messages=total_messages,
        )

        readqueueresponse.additional_properties = d
        return readqueueresponse

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
