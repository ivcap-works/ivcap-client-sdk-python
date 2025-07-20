import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect_list_item_rt_content import AspectListItemRTContent


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
        valid_from (datetime.datetime): Time this assertion became valid Example: 1996-12-19T16:39:57-08:00.
        content (Union[Unset, AspectListItemRTContent]): Attached aspect aspect
        valid_to (Union[Unset, datetime.datetime]): Time this assertion became valid Example: 1996-12-19T16:39:57-08:00.
    """

    content_type: str
    entity: str
    id: str
    schema: str
    valid_from: datetime.datetime
    content: Union[Unset, "AspectListItemRTContent"] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        entity = self.entity

        id = self.id

        schema = self.schema

        valid_from = self.valid_from.isoformat()

        content: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_dict()

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content-type": content_type,
                "entity": entity,
                "id": id,
                "schema": schema,
                "valid-from": valid_from,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aspect_list_item_rt_content import AspectListItemRTContent

        d = src_dict.copy()
        content_type = d.pop("content-type")

        entity = d.pop("entity")

        id = d.pop("id")

        schema = d.pop("schema")

        valid_from = isoparse(d.pop("valid-from"))

        _content = d.pop("content", UNSET)
        content: Union[Unset, AspectListItemRTContent]
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = AspectListItemRTContent.from_dict(_content)

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
            valid_from=valid_from,
            content=content,
            valid_to=valid_to,
        )

        aspect_list_item_rt.additional_properties = d
        return aspect_list_item_rt

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
