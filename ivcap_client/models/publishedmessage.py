from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="Publishedmessage")


@_attrs_define
class Publishedmessage:
    """
    Example:
        {'content': '{"temperature": "21", "location": "Buoy101", "timestamp": "2024-05-20T14:30:00Z"}', 'content-type':
            'application/json', 'id': 'urn:ivcap:Message identifier:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:ivcap:schema:queue:message.1'}

    Attributes:
        content (Union[Unset, File]): Message content in JSON format. Example: {"temperature": "21", "location":
            "Buoy101", "timestamp": "2024-05-20T14:30:00Z"}.
        content_type (Union[Unset, str]): Encoding type of message content (defaults to 'application/json') Example:
            application/json.
        id (Union[Unset, str]): Message identifier Example: urn:ivcap:Message
            identifier:123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema used for message Example: urn:ivcap:schema:queue:message.1.
    """

    content: Union[Unset, File] = UNSET
    content_type: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_tuple()

        content_type = self.content_type

        id = self.id

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if content_type is not UNSET:
            field_dict["content-type"] = content_type
        if id is not UNSET:
            field_dict["id"] = id
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _content = d.pop("content", UNSET)
        content: Union[Unset, File]
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = File(payload=BytesIO(_content))

        content_type = d.pop("content-type", UNSET)

        id = d.pop("id", UNSET)

        schema = d.pop("schema", UNSET)

        publishedmessage = cls(
            content=content,
            content_type=content_type,
            id=id,
            schema=schema,
        )

        publishedmessage.additional_properties = d
        return publishedmessage

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
