import datetime
from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="AspectListItemRT")


@_attrs_define
class AspectListItemRT:
    """
    Example:
        {'content': '{...}', 'content-type': 'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        content_type (str): Content-Type header, MUST be of application/json. Example: application/json.
        entity (str): Entity URN Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000.
        schema (str): Schema URN Example: urn:blue:schema.image.
        content (Union[Unset, File]): Attached aspect aspect Example: {...}.
        valid_from (Union[Unset, datetime.datetime]): Time this assertion became valid Example:
            1996-12-19T16:39:57-08:00.
        valid_to (Union[Unset, datetime.datetime]): Time this assertion became valid Example: 1996-12-19T16:39:57-08:00.
    """

    content_type: str
    entity: str
    id: str
    schema: str
    content: Union[Unset, File] = UNSET
    valid_from: Union[Unset, datetime.datetime] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        content_type = self.content_type

        entity = self.entity

        id = self.id

        schema = self.schema

        content: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_tuple()

        valid_from: Union[Unset, str] = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content-type": content_type,
                "entity": entity,
                "id": id,
                "schema": schema,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if valid_from is not UNSET:
            field_dict["valid-from"] = valid_from
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        content_type = d.pop("content-type")

        entity = d.pop("entity")

        id = d.pop("id")

        schema = d.pop("schema")

        _content = d.pop("content", UNSET)
        content: Union[Unset, File]
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = File(payload=BytesIO(_content))

        _valid_from = d.pop("valid-from", UNSET)
        valid_from: Union[Unset, datetime.datetime]
        if isinstance(_valid_from, Unset):
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        _valid_to = d.pop("valid-to", UNSET)
        valid_to: Union[Unset, datetime.datetime]
        if isinstance(_valid_to, Unset):
            valid_to = UNSET
        else:
            valid_to = isoparse(_valid_to)

        aspect_list_item_rt = cls(
            content_type=content_type,
            entity=entity,
            id=id,
            schema=schema,
            content=content,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        aspect_list_item_rt.additional_properties = d
        return aspect_list_item_rt

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
