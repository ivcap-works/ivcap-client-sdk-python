import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect_list_item_rt import AspectListItemRT
    from ..models.link_t import LinkT


T = TypeVar("T", bound="AspectListRT")


@_attrs_define
class AspectListRT:
    """
    Example:
        {'aspect-path': 'Facilis quia impedit ea.', 'at-time': '1996-12-19T16:39:57-08:00', 'entity':
            'urn:blue:image.collA.12', 'items': [{'content': '{...}', 'content-type': 'application/json', 'entity':
            'urn:blue:transect.1', 'id': 'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image', 'valid-from': '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'},
            {'content': '{...}', 'content-type': 'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}, {'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}, {'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}], 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}], 'schema': 'urn:blue:image,urn:blue:location'}

    Attributes:
        at_time (datetime.datetime): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
        items (list['AspectListItemRT']): List of aspect descriptions Example: [{'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}, {'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}].
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}].
        aspect_path (Union[Unset, str]): Optional json path to further filter on returned list Example: Cupiditate natus
            eligendi asperiores aliquam exercitationem..
        entity (Union[Unset, str]): Entity for which to request aspect Example: urn:blue:image.collA.12.
        schema (Union[Unset, str]): Optional schema to filter on Example: urn:blue:image,urn:blue:location.
    """

    at_time: datetime.datetime
    items: list["AspectListItemRT"]
    links: list["LinkT"]
    aspect_path: Union[Unset, str] = UNSET
    entity: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        at_time = self.at_time.isoformat()

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        aspect_path = self.aspect_path

        entity = self.entity

        schema = self.schema

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "at-time": at_time,
                "items": items,
                "links": links,
            }
        )
        if aspect_path is not UNSET:
            field_dict["aspect-path"] = aspect_path
        if entity is not UNSET:
            field_dict["entity"] = entity
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aspect_list_item_rt import AspectListItemRT
        from ..models.link_t import LinkT

        d = src_dict.copy()
        at_time = isoparse(d.pop("at-time"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = AspectListItemRT.from_dict(items_item_data)

            items.append(items_item)

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        aspect_path = d.pop("aspect-path", UNSET)

        entity = d.pop("entity", UNSET)

        schema = d.pop("schema", UNSET)

        aspect_list_rt = cls(
            at_time=at_time,
            items=items,
            links=links,
            aspect_path=aspect_path,
            entity=entity,
            schema=schema,
        )

        aspect_list_rt.additional_properties = d
        return aspect_list_rt

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
