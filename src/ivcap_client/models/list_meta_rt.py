import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_list_item_rt import MetadataListItemRT
    from ..models.nav_t import NavT


T = TypeVar("T", bound="ListMetaRT")


@define
class ListMetaRT:
    """
    Example:
        {'aspect-path': 'Perferendis recusandae quisquam.', 'at-time': '1996-12-19T16:39:57-08:00', 'entity-id':
            'urn:blue:image.collA.12', 'links': {'first': 'https://api.com/foo/...', 'next': 'https://api.com/foo/...',
            'self': 'https://api.com/foo/...'}, 'records': [{'aspect': '{...}', 'aspectContext': 'Iste laborum dolorem.',
            'entity': 'urn:blue:transect.1', 'record-id': 'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image'}, {'aspect': '{...}', 'aspectContext': 'Iste laborum dolorem.', 'entity':
            'urn:blue:transect.1', 'record-id': 'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image'}, {'aspect': '{...}', 'aspectContext': 'Iste laborum dolorem.', 'entity':
            'urn:blue:transect.1', 'record-id': 'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image'}], 'schema': 'urn:blue:image,urn:blue:location'}

    Attributes:
        links (NavT):  Example: {'first': 'https://api.com/foo/...', 'next': 'https://api.com/foo/...', 'self':
            'https://api.com/foo/...'}.
        records (List['MetadataListItemRT']): List of metadata records Example: [{'aspect': '{...}', 'aspectContext':
            'Iste laborum dolorem.', 'entity': 'urn:blue:transect.1', 'record-id':
            'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image'}, {'aspect': '{...}',
            'aspectContext': 'Iste laborum dolorem.', 'entity': 'urn:blue:transect.1', 'record-id':
            'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image'}].
        aspect_path (Union[Unset, str]): Optional json path to further filter on returned list Example: Magni nulla
            debitis reiciendis libero..
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        entity_id (Union[Unset, str]): Entity for which to request metadata Example: urn:blue:image.collA.12.
        schema (Union[Unset, str]): Optional schema to filter on Example: urn:blue:image,urn:blue:location.
    """

    links: "NavT"
    records: List["MetadataListItemRT"]
    aspect_path: Union[Unset, str] = UNSET
    at_time: Union[Unset, datetime.datetime] = UNSET
    entity_id: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        links = self.links.to_dict()

        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()

            records.append(records_item)

        aspect_path = self.aspect_path
        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        entity_id = self.entity_id
        schema = self.schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "links": links,
                "records": records,
            }
        )
        if aspect_path is not UNSET:
            field_dict["aspect-path"] = aspect_path
        if at_time is not UNSET:
            field_dict["at-time"] = at_time
        if entity_id is not UNSET:
            field_dict["entity-id"] = entity_id
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metadata_list_item_rt import MetadataListItemRT
        from ..models.nav_t import NavT

        d = src_dict.copy()
        links = NavT.from_dict(d.pop("links"))

        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = MetadataListItemRT.from_dict(records_item_data)

            records.append(records_item)

        aspect_path = d.pop("aspect-path", UNSET)

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        entity_id = d.pop("entity-id", UNSET)

        schema = d.pop("schema", UNSET)

        list_meta_rt = cls(
            links=links,
            records=records,
            aspect_path=aspect_path,
            at_time=at_time,
            entity_id=entity_id,
            schema=schema,
        )

        list_meta_rt.additional_properties = d
        return list_meta_rt

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
