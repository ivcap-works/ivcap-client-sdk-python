import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.artifact_list_item import ArtifactListItem
    from ..models.link_t import LinkT


T = TypeVar("T", bound="ArtifactListRT")


@_attrs_define
class ArtifactListRT:
    """
    Example:
        {'at-time': '1996-12-19T16:39:57-08:00', 'items': [{'created-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-
            type': 'image/jpeg', 'name': 'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}, {'created-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-type': 'image/jpeg', 'name': 'Fire risk for
            Lot2', 'size': 19000, 'status': 'ready'}, {'created-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-
            type': 'image/jpeg', 'name': 'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}], 'links': [{'href':
            'https://api.ivcap.net/1/....', 'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}]}

    Attributes:
        items (list['ArtifactListItem']): Artifacts Example: [{'created-at': '1996-12-19T16:39:57-08:00', 'href':
            'https://api.ivcap.net/1/orders/...', 'id': 'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-
            type': 'image/jpeg', 'name': 'Fire risk for Lot2', 'size': 19000, 'status': 'ready'}, {'created-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:artifact:123e4567-e89b-12d3-a456-426614174000', 'mime-type': 'image/jpeg', 'name': 'Fire risk for
            Lot2', 'size': 19000, 'status': 'ready'}].
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/....', 'rel': 'first', 'type': 'application/json'},
            {'href': 'https://api.ivcap.net/1/....', 'rel': 'next', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/openapi3+json'}].
        at_time (Union[Unset, datetime.datetime]): Time at which this list was valid Example: 1996-12-19T16:39:57-08:00.
    """

    items: list["ArtifactListItem"]
    links: list["LinkT"]
    at_time: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        at_time: Union[Unset, str] = UNSET
        if not isinstance(self.at_time, Unset):
            at_time = self.at_time.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "links": links,
            }
        )
        if at_time is not UNSET:
            field_dict["at-time"] = at_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.artifact_list_item import ArtifactListItem
        from ..models.link_t import LinkT

        d = src_dict.copy()
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ArtifactListItem.from_dict(items_item_data)

            items.append(items_item)

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        _at_time = d.pop("at-time", UNSET)
        at_time: Union[Unset, datetime.datetime]
        if isinstance(_at_time, Unset):
            at_time = UNSET
        else:
            at_time = isoparse(_at_time)

        artifact_list_rt = cls(
            items=items,
            links=links,
            at_time=at_time,
        )

        artifact_list_rt.additional_properties = d
        return artifact_list_rt

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
