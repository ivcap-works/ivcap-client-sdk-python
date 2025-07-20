import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publishedmessage import Publishedmessage


T = TypeVar("T", bound="MessageList")


@_attrs_define
class MessageList:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'messages': [{'content': '{"temperature": "21", "location": "Buoy101",
            "timestamp": "2024-05-20T14:30:00Z"}', 'content-type': 'application/json', 'id': 'urn:ivcap:Message
            identifier:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:ivcap:schema:queue:message.1'}, {'content':
            '{"temperature": "21", "location": "Buoy101", "timestamp": "2024-05-20T14:30:00Z"}', 'content-type':
            'application/json', 'id': 'urn:ivcap:Message identifier:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:ivcap:schema:queue:message.1'}, {'content': '{"temperature": "21", "location": "Buoy101", "timestamp":
            "2024-05-20T14:30:00Z"}', 'content-type': 'application/json', 'id': 'urn:ivcap:Message
            identifier:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:ivcap:schema:queue:message.1'}]}

    Attributes:
        messages (list['Publishedmessage']): Messages in the queue Example: [{'content': '{"temperature": "21",
            "location": "Buoy101", "timestamp": "2024-05-20T14:30:00Z"}', 'content-type': 'application/json', 'id':
            'urn:ivcap:Message identifier:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:ivcap:schema:queue:message.1'}, {'content': '{"temperature": "21", "location": "Buoy101", "timestamp":
            "2024-05-20T14:30:00Z"}', 'content-type': 'application/json', 'id': 'urn:ivcap:Message
            identifier:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:ivcap:schema:queue:message.1'}].
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
    """

    messages: list["Publishedmessage"]
    at_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        messages = []
        for messages_item_data in self.messages:
            messages_item = messages_item_data.to_dict()
            messages.append(messages_item)

        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "messages": messages,
            }
        )
        if at_time is not UNSET:
            field_dict["at-time"] = at_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.publishedmessage import Publishedmessage

        d = src_dict.copy()
        messages = []
        _messages = d.pop("messages")
        for messages_item_data in _messages:
            messages_item = Publishedmessage.from_dict(messages_item_data)

            messages.append(messages_item)

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        message_list = cls(
            messages=messages,
            at_time=at_time,
        )

        message_list.additional_properties = d
        return message_list

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
