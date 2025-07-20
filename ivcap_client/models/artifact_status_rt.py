import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artifact_status_rt_status import ArtifactStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT


T = TypeVar("T", bound="ArtifactStatusRT")


@_attrs_define
class ArtifactStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'cache-of': 'urn:ivcap:artifact:00000',
            'created-at': '1996-12-19T16:39:57-08:00', 'data-href': 'https://api.ivcap.net/1/artifacts/.../blob', 'etag':
            '00000-0000123', 'id': 'urn:ivcap:Artifact ID:123e4567-e89b-12d3-a456-426614174000', 'last-modified-at':
            '1996-12-19T16:39:57-08:00', 'links': [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}], 'mime-type': 'application/json', 'name': 'Fire risk per LGA',
            'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'size': 7909153619056419590, 'status':
            'partial'}

    Attributes:
        id (str): Artifact ID Example: urn:ivcap:Artifact ID:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        status (ArtifactStatusRTStatus): Artifact status Example: pending.
        account (Union[Unset, str]): Reference to billable account Example:
            urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        cache_of (Union[Unset, str]): URL of object this artifact is caching Example: urn:ivcap:artifact:00000.
        created_at (Union[Unset, datetime.datetime]): DateTime artifact was created Example: 1996-12-19T16:39:57-08:00.
        data_href (Union[Unset, str]):  Example: https://api.ivcap.net/1/artifacts/.../blob.
        etag (Union[Unset, str]): ETAG of artifact Example: 00000-0000123.
        last_modified_at (Union[Unset, datetime.datetime]): DateTime artifact was last modified Example:
            1996-12-19T16:39:57-08:00.
        mime_type (Union[Unset, str]): Mime-type of data Example: application/json.
        name (Union[Unset, str]): Optional name Example: Fire risk per LGA.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        size (Union[Unset, int]): Size of data Example: 2839568718113232130.
    """

    id: str
    links: list["LinkT"]
    status: ArtifactStatusRTStatus
    account: Union[Unset, str] = UNSET
    cache_of: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    data_href: Union[Unset, str] = UNSET
    etag: Union[Unset, str] = UNSET
    last_modified_at: Union[Unset, datetime.datetime] = UNSET
    mime_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        status = self.status.value

        account = self.account

        cache_of = self.cache_of

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        data_href = self.data_href

        etag = self.etag

        last_modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_modified_at, Unset):
            last_modified_at = self.last_modified_at.isoformat()

        mime_type = self.mime_type

        name = self.name

        policy = self.policy

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "links": links,
                "status": status,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if cache_of is not UNSET:
            field_dict["cache-of"] = cache_of
        if created_at is not UNSET:
            field_dict["created-at"] = created_at
        if data_href is not UNSET:
            field_dict["data-href"] = data_href
        if etag is not UNSET:
            field_dict["etag"] = etag
        if last_modified_at is not UNSET:
            field_dict["last-modified-at"] = last_modified_at
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT

        d = src_dict.copy()
        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        status = ArtifactStatusRTStatus(d.pop("status"))

        account = d.pop("account", UNSET)

        cache_of = d.pop("cache-of", UNSET)

        _created_at = d.pop("created-at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        data_href = d.pop("data-href", UNSET)

        etag = d.pop("etag", UNSET)

        _last_modified_at = d.pop("last-modified-at", UNSET)
        last_modified_at: Union[Unset, datetime.datetime]
        if isinstance(_last_modified_at, Unset):
            last_modified_at = UNSET
        else:
            last_modified_at = isoparse(_last_modified_at)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        size = d.pop("size", UNSET)

        artifact_status_rt = cls(
            id=id,
            links=links,
            status=status,
            account=account,
            cache_of=cache_of,
            created_at=created_at,
            data_href=data_href,
            etag=etag,
            last_modified_at=last_modified_at,
            mime_type=mime_type,
            name=name,
            policy=policy,
            size=size,
        )

        artifact_status_rt.additional_properties = d
        return artifact_status_rt

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
