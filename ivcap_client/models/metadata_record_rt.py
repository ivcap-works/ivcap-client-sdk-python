import datetime
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT


T = TypeVar("T", bound="MetadataRecordRT")


@_attrs_define
class MetadataRecordRT:
    """
    Example:
        {'aspect': '{...}', 'asserter': 'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'entity':
            'urn:blue:transect.1', 'id': 'urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'revoker': 'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image', 'valid-from': '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        aspect (File): Attached metadata aspect Example: {...}.
        asserter (str): Entity asserting this metadata record at 'valid-from' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        entity (str): Entity ID Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        schema (str): Schema ID Example: urn:blue:schema.image.
        valid_from (datetime.datetime): Time this record was asserted Example: 1996-12-19T16:39:57-08:00.
        revoker (Union[Unset, str]): Entity revoking this record at 'valid-to' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        valid_to (Union[Unset, datetime.datetime]): Time this record was retracted Example: 1996-12-19T16:39:57-08:00.
    """

    aspect: File
    asserter: str
    entity: str
    id: str
    links: list["LinkT"]
    schema: str
    valid_from: datetime.datetime
    revoker: Union[Unset, str] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        aspect = self.aspect.to_tuple()

        asserter = self.asserter

        entity = self.entity

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        schema = self.schema

        valid_from = self.valid_from.isoformat()

        revoker = self.revoker

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aspect": aspect,
                "asserter": asserter,
                "entity": entity,
                "id": id,
                "links": links,
                "schema": schema,
                "valid-from": valid_from,
            }
        )
        if revoker is not UNSET:
            field_dict["revoker"] = revoker
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT

        d = src_dict.copy()
        aspect = File(payload=BytesIO(d.pop("aspect")))

        asserter = d.pop("asserter")

        entity = d.pop("entity")

        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        schema = d.pop("schema")

        valid_from = isoparse(d.pop("valid-from"))

        revoker = d.pop("revoker", UNSET)

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
            id=id,
            links=links,
            schema=schema,
            valid_from=valid_from,
            revoker=revoker,
            valid_to=valid_to,
        )

        metadata_record_rt.additional_properties = d
        return metadata_record_rt

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
