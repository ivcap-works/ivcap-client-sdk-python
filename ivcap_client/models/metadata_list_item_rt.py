from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_list_item_rt_aspect import MetadataListItemRTAspect


T = TypeVar("T", bound="MetadataListItemRT")


@_attrs_define
class MetadataListItemRT:
    """
    Example:
        {'aspect': '{...}', 'aspect-context': '{...}', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:metadata:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image'}

    Attributes:
        entity (str): Entity ID Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:metadata:123e4567-e89b-12d3-a456-426614174000.
        schema (str): Schema ID Example: urn:blue:schema.image.
        aspect (Union[Unset, MetadataListItemRTAspect]): Attached metadata aspect Example: {...}.
        aspect_context (Union[Unset, str]): If aspectPath was defined, this is what matched the query Example: {...}.
    """

    entity: str
    id: str
    schema: str
    aspect: Union[Unset, "MetadataListItemRTAspect"] = UNSET
    aspect_context: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entity = self.entity

        id = self.id

        schema = self.schema

        aspect: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aspect, Unset):
            aspect = self.aspect.to_dict()

        aspect_context = self.aspect_context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entity": entity,
                "id": id,
                "schema": schema,
            }
        )
        if aspect is not UNSET:
            field_dict["aspect"] = aspect
        if aspect_context is not UNSET:
            field_dict["aspect-context"] = aspect_context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metadata_list_item_rt_aspect import MetadataListItemRTAspect

        d = src_dict.copy()
        entity = d.pop("entity")

        id = d.pop("id")

        schema = d.pop("schema")

        _aspect = d.pop("aspect", UNSET)
        aspect: Union[Unset, MetadataListItemRTAspect]
        if isinstance(_aspect, Unset):
            aspect = UNSET
        else:
            aspect = MetadataListItemRTAspect.from_dict(_aspect)

        aspect_context = d.pop("aspect-context", UNSET)

        metadata_list_item_rt = cls(
            entity=entity,
            id=id,
            schema=schema,
            aspect=aspect,
            aspect_context=aspect_context,
        )

        metadata_list_item_rt.additional_properties = d
        return metadata_list_item_rt

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
