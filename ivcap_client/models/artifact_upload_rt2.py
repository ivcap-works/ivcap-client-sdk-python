from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artifact_upload_rt2_status import ArtifactUploadRT2Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT


T = TypeVar("T", bound="ArtifactUploadRT2")


@_attrs_define
class ArtifactUploadRT2:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'cache-of': 'urn:ivcap:artifact:00000',
            'created-at': '1996-12-19T16:39:57-08:00', 'data-href': 'https://api.ivcap.net/1/artifacts/.../blob', 'etag':
            '00000-0000123', 'id': 'urn:ivcap:Artifact ID:123e4567-e89b-12d3-a456-426614174000', 'last-modified-at':
            '1996-12-19T16:39:57-08:00', 'links': [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}], 'mime-type': 'application/json', 'name': 'Fire risk per LGA',
            'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'size': 7299359519116713580, 'status':
            'ready'}

    Attributes:
        id (str): Artifact ID Example: urn:ivcap:Artifact ID:123e4567-e89b-12d3-a456-426614174000.
        links (list[LinkT]):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        status (ArtifactUploadRT2Status): Artifact status Example: pending.
        account (str | Unset): Reference to billable account Example:
            urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        cache_of (str | Unset): URL of object this artifact is caching Example: urn:ivcap:artifact:00000.
        created_at (datetime.datetime | Unset): DateTime artifact was created Example: 1996-12-19T16:39:57-08:00.
        data_href (str | Unset):  Example: https://api.ivcap.net/1/artifacts/.../blob.
        etag (str | Unset): ETAG of artifact Example: 00000-0000123.
        last_modified_at (datetime.datetime | Unset): DateTime artifact was last modified Example:
            1996-12-19T16:39:57-08:00.
        mime_type (str | Unset): Mime-type of data Example: application/json.
        name (str | Unset): Optional name Example: Fire risk per LGA.
        policy (str | Unset): Reference to policy used Example: urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        size (int | Unset): Size of data Example: 6612574515353717636.
    """

    id: str
    links: list[LinkT]
    status: ArtifactUploadRT2Status
    account: str | Unset = UNSET
    cache_of: str | Unset = UNSET
    created_at: datetime.datetime | Unset = UNSET
    data_href: str | Unset = UNSET
    etag: str | Unset = UNSET
    last_modified_at: datetime.datetime | Unset = UNSET
    mime_type: str | Unset = UNSET
    name: str | Unset = UNSET
    policy: str | Unset = UNSET
    size: int | Unset = UNSET
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

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        data_href = self.data_href

        etag = self.etag

        last_modified_at: str | Unset = UNSET
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.link_t import LinkT

        d = dict(src_dict)
        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        status = ArtifactUploadRT2Status(d.pop("status"))

        account = d.pop("account", UNSET)

        cache_of = d.pop("cache-of", UNSET)

        _created_at = d.pop("created-at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        data_href = d.pop("data-href", UNSET)

        etag = d.pop("etag", UNSET)

        _last_modified_at = d.pop("last-modified-at", UNSET)
        last_modified_at: datetime.datetime | Unset
        if isinstance(_last_modified_at, Unset):
            last_modified_at = UNSET
        else:
            last_modified_at = isoparse(_last_modified_at)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        size = d.pop("size", UNSET)

        artifact_upload_rt2 = cls(
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

        artifact_upload_rt2.additional_properties = d
        return artifact_upload_rt2

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
