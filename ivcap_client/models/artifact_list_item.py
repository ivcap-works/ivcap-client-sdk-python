import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.artifact_list_item_status import ArtifactListItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArtifactListItem")


@_attrs_define
class ArtifactListItem:
    """
    Example:
        {'created-at': '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-type': 'image/jpeg', 'name': 'Fire risk for
            Lot2', 'size': 19000, 'status': 'ready'}

    Attributes:
        created_at (datetime.datetime): time this artifact was created Example: 1996-12-19T16:39:57-08:00.
        href (str):  Example: https://api.ivcap.net/1/orders/....
        id (str): ID Example: urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000.
        status (ArtifactListItemStatus): Artifact status Example: ready.
        mime_type (Union[Unset, str]): Mime (content) type of artifact Example: image/jpeg.
        name (Union[Unset, str]): Optional name Example: Fire risk for Lot2.
        size (Union[Unset, int]): Size of artifact in bytes Example: 19000.
    """

    created_at: datetime.datetime
    href: str
    id: str
    status: ArtifactListItemStatus
    mime_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        href = self.href

        id = self.id

        status = self.status.value

        mime_type = self.mime_type

        name = self.name

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created-at": created_at,
                "href": href,
                "id": id,
                "status": status,
            }
        )
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created-at"))

        href = d.pop("href")

        id = d.pop("id")

        status = ArtifactListItemStatus(d.pop("status"))

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        artifact_list_item = cls(
            created_at=created_at,
            href=href,
            id=id,
            status=status,
            mime_type=mime_type,
            name=name,
            size=size,
        )

        artifact_list_item.additional_properties = d
        return artifact_list_item

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
