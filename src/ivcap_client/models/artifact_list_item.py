from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..models.artifact_list_item_status import ArtifactListItemStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_t import SelfT


T = TypeVar("T", bound="ArtifactListItem")


@define
class ArtifactListItem:
    """
    Example:
        {'id': 'cayp:artifact:0000-000', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Ipsam deleniti magnam nihil et.'}, 'mime-type': 'image/jpeg', 'name':
            'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}

    Attributes:
        links (SelfT):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Consequatur adipisci.'}.
        id (Union[Unset, str]): Artifact ID Example: cayp:artifact:0000-000.
        mime_type (Union[Unset, str]): Mime (content) type of artifact Example: image/jpeg.
        name (Union[Unset, str]): Optional name Example: Fire risk for Lot2.
        size (Union[Unset, int]): Size of aritfact in bytes Example: 19000.
        status (Union[Unset, ArtifactListItemStatus]): Artifact status Example: ready.
    """

    links: "SelfT"
    id: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    status: Union[Unset, ArtifactListItemStatus] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        links = self.links.to_dict()

        id = self.id
        mime_type = self.mime_type
        name = self.name
        size = self.size
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "links": links,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.self_t import SelfT

        d = src_dict.copy()
        links = SelfT.from_dict(d.pop("links"))

        id = d.pop("id", UNSET)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ArtifactListItemStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ArtifactListItemStatus(_status)

        artifact_list_item = cls(
            links=links,
            id=id,
            mime_type=mime_type,
            name=name,
            size=size,
            status=status,
        )

        artifact_list_item.additional_properties = d
        return artifact_list_item

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
