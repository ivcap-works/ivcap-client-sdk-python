import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_list_item import ArtifactListItem
    from ..models.nav_t import NavT


T = TypeVar("T", bound="ArtifactListRT")


@define
class ArtifactListRT:
    """
    Example:
        {'artifacts': [{'id': 'cayp:artifact:0000-000', 'links': {'describedBy': {'href': 'https://api.com/swagger/...',
            'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'mime-type': 'image/jpeg', 'name': 'Fire risk
            for Lot2', 'size': 19000, 'status': 'ready'}, {'id': 'cayp:artifact:0000-000', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'mime-type':
            'image/jpeg', 'name': 'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}], 'at-time':
            '1996-12-19T16:39:57-08:00', 'links': {'first': 'https://api.com/foo/...', 'next': 'https://api.com/foo/...',
            'self': 'https://api.com/foo/...'}}

    Attributes:
        artifacts (List['ArtifactListItem']): Artifacts Example: [{'id': 'cayp:artifact:0000-000', 'links':
            {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum
            odit.'}, 'mime-type': 'image/jpeg', 'name': 'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}, {'id':
            'cayp:artifact:0000-000', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'mime-type': 'image/jpeg', 'name': 'Fire risk for
            Lot2', 'size': 19000, 'status': 'ready'}].
        links (NavT):  Example: {'first': 'https://api.com/foo/...', 'next': 'https://api.com/foo/...', 'self':
            'https://api.com/foo/...'}.
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
    """

    artifacts: List["ArtifactListItem"]
    links: "NavT"
    at_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        artifacts = []
        for artifacts_item_data in self.artifacts:
            artifacts_item = artifacts_item_data.to_dict()

            artifacts.append(artifacts_item)

        links = self.links.to_dict()

        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "artifacts": artifacts,
                "links": links,
            }
        )
        if at_time is not UNSET:
            field_dict["at-time"] = at_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.artifact_list_item import ArtifactListItem
        from ..models.nav_t import NavT

        d = src_dict.copy()
        artifacts = []
        _artifacts = d.pop("artifacts")
        for artifacts_item_data in _artifacts:
            artifacts_item = ArtifactListItem.from_dict(artifacts_item_data)

            artifacts.append(artifacts_item)

        links = NavT.from_dict(d.pop("links"))

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        artifact_list_rt = cls(
            artifacts=artifacts,
            links=links,
            at_time=at_time,
        )

        artifact_list_rt.additional_properties = d
        return artifact_list_rt

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
