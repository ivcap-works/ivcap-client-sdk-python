from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..models.artifact_status_rt_status import ArtifactStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref_t import RefT
    from ..models.self_t import SelfT


T = TypeVar("T", bound="ArtifactStatusRT")


@define
class ArtifactStatusRT:
    """
    Example:
        {'account': {'id': 'http://beahan.net/laurie', 'links': {'describedBy': {'href': 'https://api.com/swagger/...',
            'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}, 'cache-of': 'Quia nesciunt.', 'created-at':
            '2022-01-01', 'data': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'etag': 'Voluptatem rerum qui amet earum.', 'id':
            'type:scope:name', 'last-modified-at': '2022-01-01', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'location':
            'Distinctio dolorum blanditiis quos officia nemo et.', 'mime-type': 'Libero voluptatem quis quam repudiandae
            dolor.', 'name': 'Fire risk per LGA', 'policy': {'id': 'http://beahan.net/laurie', 'links': {'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}},
            'size': 584529819162657777, 'status': 'partial', 'tus-offset': 2098596842068964345, 'tus-resumable': 'Voluptatum
            qui earum inventore.'}

    Attributes:
        id (str): Artifact ID Example: type:scope:name.
        links (SelfT):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'At qui.'}.
        status (ArtifactStatusRTStatus): Artifact status Example: ready.
        account (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        cache_of (Union[Unset, str]): URL of object this artifact is caching Example: Hic dignissimos vero consequatur..
        created_at (Union[Unset, str]): DateTime artifact was created Example: 2022-01-01.
        data (Union[Unset, SelfT]):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'At qui.'}.
        etag (Union[Unset, str]): ETAG of artifact Example: In similique..
        last_modified_at (Union[Unset, str]): DateTime artifact was last modified Example: 2022-01-01.
        location (Union[Unset, str]): link back to record Example: Voluptas consectetur quia sint aut odit..
        mime_type (Union[Unset, str]): Mime-type of data Example: Reprehenderit quia..
        name (Union[Unset, str]): Optional name Example: Fire risk per LGA.
        policy (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        size (Union[Unset, int]): Size of data Example: 9098245488094500492.
        tus_offset (Union[Unset, int]): TUS offset for partially uploaded content Example: 1538876244134645216.
        tus_resumable (Union[Unset, str]): indicate version of TUS supported Example: Nulla quo ut asperiores temporibus
            quia..
    """

    id: str
    links: "SelfT"
    status: ArtifactStatusRTStatus
    account: Union[Unset, "RefT"] = UNSET
    cache_of: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    data: Union[Unset, "SelfT"] = UNSET
    etag: Union[Unset, str] = UNSET
    last_modified_at: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, "RefT"] = UNSET
    size: Union[Unset, int] = UNSET
    tus_offset: Union[Unset, int] = UNSET
    tus_resumable: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        links = self.links.to_dict()

        status = self.status.value

        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        cache_of = self.cache_of
        created_at = self.created_at
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        etag = self.etag
        last_modified_at = self.last_modified_at
        location = self.location
        mime_type = self.mime_type
        name = self.name
        policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        size = self.size
        tus_offset = self.tus_offset
        tus_resumable = self.tus_resumable

        field_dict: Dict[str, Any] = {}
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
        if data is not UNSET:
            field_dict["data"] = data
        if etag is not UNSET:
            field_dict["etag"] = etag
        if last_modified_at is not UNSET:
            field_dict["last-modified-at"] = last_modified_at
        if location is not UNSET:
            field_dict["location"] = location
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if size is not UNSET:
            field_dict["size"] = size
        if tus_offset is not UNSET:
            field_dict["tus-offset"] = tus_offset
        if tus_resumable is not UNSET:
            field_dict["tus-resumable"] = tus_resumable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ref_t import RefT
        from ..models.self_t import SelfT

        d = src_dict.copy()
        id = d.pop("id")

        links = SelfT.from_dict(d.pop("links"))

        status = ArtifactStatusRTStatus(d.pop("status"))

        _account = d.pop("account", UNSET)
        account: Union[Unset, RefT]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = RefT.from_dict(_account)

        cache_of = d.pop("cache-of", UNSET)

        created_at = d.pop("created-at", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, SelfT]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = SelfT.from_dict(_data)

        etag = d.pop("etag", UNSET)

        last_modified_at = d.pop("last-modified-at", UNSET)

        location = d.pop("location", UNSET)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        _policy = d.pop("policy", UNSET)
        policy: Union[Unset, RefT]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = RefT.from_dict(_policy)

        size = d.pop("size", UNSET)

        tus_offset = d.pop("tus-offset", UNSET)

        tus_resumable = d.pop("tus-resumable", UNSET)

        artifact_status_rt = cls(
            id=id,
            links=links,
            status=status,
            account=account,
            cache_of=cache_of,
            created_at=created_at,
            data=data,
            etag=etag,
            last_modified_at=last_modified_at,
            location=location,
            mime_type=mime_type,
            name=name,
            policy=policy,
            size=size,
            tus_offset=tus_offset,
            tus_resumable=tus_resumable,
        )

        artifact_status_rt.additional_properties = d
        return artifact_status_rt

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
