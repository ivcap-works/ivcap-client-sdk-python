from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="MetadataListItemRT")


@define
class MetadataListItemRT:
    """
    Example:
        {'aspect': '{...}', 'aspectContext': 'Sapiente possimus commodi qui sint aut.', 'entity': 'urn:blue:transect.1',
            'record-id': 'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image'}

    Attributes:
        aspect (Union[Unset, File]): Attached metadata aspect Example: {...}.
        aspect_context (Union[Unset, File]): If aspectPath was defined, this is what matched the query Example:
            Architecto facere veniam dolorem velit quia..
        entity (Union[Unset, str]): Entity ID Example: urn:blue:transect.1.
        record_id (Union[Unset, str]): Record ID Example: urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000.
        schema (Union[Unset, str]): Schema ID Example: urn:blue:schema.image.
    """

    aspect: Union[Unset, File] = UNSET
    aspect_context: Union[Unset, File] = UNSET
    entity: Union[Unset, str] = UNSET
    record_id: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspect: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.aspect, Unset):
            aspect = self.aspect.to_tuple()

        aspect_context: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.aspect_context, Unset):
            aspect_context = self.aspect_context.to_tuple()

        entity = self.entity
        record_id = self.record_id
        schema = self.schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspect is not UNSET:
            field_dict["aspect"] = aspect
        if aspect_context is not UNSET:
            field_dict["aspectContext"] = aspect_context
        if entity is not UNSET:
            field_dict["entity"] = entity
        if record_id is not UNSET:
            field_dict["record-id"] = record_id
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _aspect = d.pop("aspect", UNSET)
        aspect: Union[Unset, File]
        if isinstance(_aspect, Unset):
            aspect = UNSET
        else:
            aspect = File(payload=BytesIO(_aspect))

        _aspect_context = d.pop("aspectContext", UNSET)
        aspect_context: Union[Unset, File]
        if isinstance(_aspect_context, Unset):
            aspect_context = UNSET
        else:
            aspect_context = File(payload=BytesIO(_aspect_context))

        entity = d.pop("entity", UNSET)

        record_id = d.pop("record-id", UNSET)

        schema = d.pop("schema", UNSET)

        metadata_list_item_rt = cls(
            aspect=aspect,
            aspect_context=aspect_context,
            entity=entity,
            record_id=record_id,
            schema=schema,
        )

        metadata_list_item_rt.additional_properties = d
        return metadata_list_item_rt

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
