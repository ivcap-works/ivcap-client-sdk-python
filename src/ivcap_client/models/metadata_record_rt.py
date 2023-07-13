import datetime
from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, File, FileJsonType, Unset

T = TypeVar("T", bound="MetadataRecordRT")


@attr.s(auto_attribs=True)
class MetadataRecordRT:
    """
    Example:
        {'aspect': '{...}', 'asserter': '...', 'entity': 'urn:blue:transect.1', 'record-id':
            'urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000', 'revoker': '...', 'schema': 'urn:blue:schema.image',
            'valid-from': '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        aspect (Union[Unset, File]): Attached metadata aspect Example: {...}.
        asserter (Union[Unset, str]): Entity asserting this metadata record at 'valid-from' Example: ....
        entity (Union[Unset, str]): Entity ID Example: urn:blue:transect.1.
        record_id (Union[Unset, str]): Record ID Example: urn:ivcap:record.123e4567-e89b-12d3-a456-426614174000.
        revoker (Union[Unset, datetime.datetime]): Entity revoking this record at 'valid-to' Example: ....
        schema (Union[Unset, str]): Schema ID Example: urn:blue:schema.image.
        valid_from (Union[Unset, datetime.datetime]): Time this record was asserted Example: 1996-12-19T16:39:57-08:00.
        valid_to (Union[Unset, datetime.datetime]): Time this record was revoked Example: 1996-12-19T16:39:57-08:00.
    """

    aspect: Union[Unset, File] = UNSET
    asserter: Union[Unset, str] = UNSET
    entity: Union[Unset, str] = UNSET
    record_id: Union[Unset, str] = UNSET
    revoker: Union[Unset, datetime.datetime] = UNSET
    schema: Union[Unset, str] = UNSET
    valid_from: Union[Unset, datetime.datetime] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aspect: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.aspect, Unset):
            aspect = self.aspect.to_tuple()

        asserter = self.asserter
        entity = self.entity
        record_id = self.record_id
        revoker: Union[Unset, str] = UNSET
        if not isinstance(self.revoker, Unset):
            revoker = self.revoker.isoformat()

        schema = self.schema
        valid_from: Union[Unset, str] = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aspect is not UNSET:
            field_dict["aspect"] = aspect
        if asserter is not UNSET:
            field_dict["asserter"] = asserter
        if entity is not UNSET:
            field_dict["entity"] = entity
        if record_id is not UNSET:
            field_dict["record-id"] = record_id
        if revoker is not UNSET:
            field_dict["revoker"] = revoker
        if schema is not UNSET:
            field_dict["schema"] = schema
        if valid_from is not UNSET:
            field_dict["valid-from"] = valid_from
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

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

        asserter = d.pop("asserter", UNSET)

        entity = d.pop("entity", UNSET)

        record_id = d.pop("record-id", UNSET)

        _revoker = d.pop("revoker", UNSET)
        revoker: Union[Unset, datetime.datetime]
        if isinstance(_revoker, Unset):
            revoker = UNSET
        else:
            revoker = isoparse(_revoker)

        schema = d.pop("schema", UNSET)

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

        metadata_record_rt = cls(
            aspect=aspect,
            asserter=asserter,
            entity=entity,
            record_id=record_id,
            revoker=revoker,
            schema=schema,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        metadata_record_rt.additional_properties = d
        return metadata_record_rt

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
