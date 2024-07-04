import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aspect_rt_content import AspectRTContent
    from ..models.link_t import LinkT


T = TypeVar("T", bound="AspectRT")


@_attrs_define
class AspectRT:
    """
    Example:
        {'asserter': 'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'retracter': 'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'schema':
            'urn:blue:schema.image', 'valid-from': '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        asserter (str): Entity asserting this metadata record at 'valid-from' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        content (AspectRTContent): Attached aspect aspect
        content_type (str): Content-Type header, MUST be of application/json. Example: application/json.
        entity (str): Entity URN Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000.
        links (List['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        schema (str): Schema URN Example: urn:blue:schema.image.
        valid_from (datetime.datetime): Time this record was asserted Example: 1996-12-19T16:39:57-08:00.
        retracter (Union[Unset, str]): Entity retracting this record at 'valid-to' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        valid_to (Union[Unset, datetime.datetime]): Time this record was retracted Example: 1996-12-19T16:39:57-08:00.
    """

    asserter: str
    content: "AspectRTContent"
    content_type: str
    entity: str
    id: str
    links: List["LinkT"]
    schema: str
    valid_from: datetime.datetime
    retracter: Union[Unset, str] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        asserter = self.asserter

        content = self.content.to_dict()

        content_type = self.content_type

        entity = self.entity

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        schema = self.schema

        valid_from = self.valid_from.isoformat()

        retracter = self.retracter

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asserter": asserter,
                "content": content,
                "content-type": content_type,
                "entity": entity,
                "id": id,
                "links": links,
                "schema": schema,
                "valid-from": valid_from,
            }
        )
        if retracter is not UNSET:
            field_dict["retracter"] = retracter
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.aspect_rt_content import AspectRTContent
        from ..models.link_t import LinkT

        d = src_dict.copy()
        asserter = d.pop("asserter")

        content = AspectRTContent.from_dict(d.pop("content"))

        content_type = d.pop("content-type")

        entity = d.pop("entity")

        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        schema = d.pop("schema")

        valid_from = isoparse(d.pop("valid-from"))

        retracter = d.pop("retracter", UNSET)

        _valid_to = d.pop("valid-to", UNSET)
        valid_to: Union[Unset, datetime.datetime]
        if isinstance(_valid_to, Unset):
            valid_to = UNSET
        else:
            valid_to = isoparse(_valid_to)

        aspect_rt = cls(
            asserter=asserter,
            content=content,
            content_type=content_type,
            entity=entity,
            id=id,
            links=links,
            schema=schema,
            valid_from=valid_from,
            retracter=retracter,
            valid_to=valid_to,
        )

        aspect_rt.additional_properties = d
        return aspect_rt

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
