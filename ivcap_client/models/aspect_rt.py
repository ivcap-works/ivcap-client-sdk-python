import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'asserter':
            'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'content': '{...}', 'content-type':
            'application/json', 'entity': 'urn:blue:transect.1', 'id':
            'urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'replaces':
            'urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000', 'retracter':
            'urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000', 'schema': 'urn:blue:schema.image', 'valid-from':
            '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        asserter (str): Entity asserting this metadata record at 'valid-from' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        content (AspectRTContent): Attached aspect aspect
        content_type (str): Content-Type header, MUST be of application/json. Example: application/json.
        entity (str): Entity URN Example: urn:blue:transect.1.
        id (str): ID Example: urn:ivcap:record:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        policy (str): Reference to policy used Example: urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        schema (str): Schema URN Example: urn:blue:schema.image.
        valid_from (datetime.datetime): Time this record was asserted Example: 1996-12-19T16:39:57-08:00.
        replaces (Union[Unset, str]): Reference to retracted aspect record this record is replacing Example:
            urn:ivcap:aspect:123e4567-e89b-12d3-a456-426614174000.
        retracter (Union[Unset, str]): Entity retracting this record at 'valid-to' Example:
            urn:ivcap:principal:123e4567-e89b-12d3-a456-426614174000.
        valid_to (Union[Unset, datetime.datetime]): Time this record was retracted Example: 1996-12-19T16:39:57-08:00.
    """

    account: str
    asserter: str
    content: "AspectRTContent"
    content_type: str
    entity: str
    id: str
    links: list["LinkT"]
    policy: str
    schema: str
    valid_from: datetime.datetime
    replaces: Union[Unset, str] = UNSET
    retracter: Union[Unset, str] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        asserter = self.asserter

        content = self.content.to_dict()

        content_type = self.content_type

        entity = self.entity

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        policy = self.policy

        schema = self.schema

        valid_from = self.valid_from.isoformat()

        replaces = self.replaces

        retracter = self.retracter

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "asserter": asserter,
                "content": content,
                "content-type": content_type,
                "entity": entity,
                "id": id,
                "links": links,
                "policy": policy,
                "schema": schema,
                "valid-from": valid_from,
            }
        )
        if replaces is not UNSET:
            field_dict["replaces"] = replaces
        if retracter is not UNSET:
            field_dict["retracter"] = retracter
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.aspect_rt_content import AspectRTContent
        from ..models.link_t import LinkT

        d = src_dict.copy()
        account = d.pop("account")

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

        policy = d.pop("policy")

        schema = d.pop("schema")

        valid_from = isoparse(d.pop("valid-from"))

        replaces = d.pop("replaces", UNSET)

        retracter = d.pop("retracter", UNSET)

        _valid_to = d.pop("valid-to", UNSET)
        valid_to: Union[Unset, datetime.datetime]
        if isinstance(_valid_to, Unset):
            valid_to = UNSET
        else:
            valid_to = isoparse(_valid_to)

        aspect_rt = cls(
            account=account,
            asserter=asserter,
            content=content,
            content_type=content_type,
            entity=entity,
            id=id,
            links=links,
            policy=policy,
            schema=schema,
            valid_from=valid_from,
            replaces=replaces,
            retracter=retracter,
            valid_to=valid_to,
        )

        aspect_rt.additional_properties = d
        return aspect_rt

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
