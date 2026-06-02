from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceListItemT")


@_attrs_define
class ServiceListItemT:
    """
    Example:
        {'controller-schema': 'Cumque consequatur at est.', 'description': 'Some lengthy description of fire risk',
            'href': 'https://api.ivcap.net/1/services/...', 'id': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000',
            'name': 'Fire risk for region', 'tags': ['tag1', 'tag2'], 'valid-from': '1996-12-19T16:39:57-08:00', 'valid-to':
            '1996-12-19T16:39:57-08:00'}

    Attributes:
        controller_schema (str): type of controller used for this service Example: Corrupti laborum qui incidunt..
        href (str):  Example: https://api.ivcap.net/1/services/....
        id (str): ID Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        description (str | Unset): Optional description of the service Example: Some lengthy description of fire risk.
        name (str | Unset): Optional customer provided name Example: Fire risk for region.
        tags (list[str] | Unset): Optional tags defined for service to help in categorising them Example: ['tag1',
            'tag2'].
        valid_from (datetime.datetime | Unset): time this service has been available from Example:
            1996-12-19T16:39:57-08:00.
        valid_to (datetime.datetime | Unset): time this service has been available to Example:
            1996-12-19T16:39:57-08:00.
    """

    controller_schema: str
    href: str
    id: str
    description: str | Unset = UNSET
    name: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    valid_from: datetime.datetime | Unset = UNSET
    valid_to: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        controller_schema = self.controller_schema

        href = self.href

        id = self.id

        description = self.description

        name = self.name

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        valid_from: str | Unset = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_to: str | Unset = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "controller-schema": controller_schema,
                "href": href,
                "id": id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if valid_from is not UNSET:
            field_dict["valid-from"] = valid_from
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        controller_schema = d.pop("controller-schema")

        href = d.pop("href")

        id = d.pop("id")

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _valid_from = d.pop("valid-from", UNSET)
        valid_from: datetime.datetime | Unset
        if isinstance(_valid_from, Unset):
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        _valid_to = d.pop("valid-to", UNSET)
        valid_to: datetime.datetime | Unset
        if isinstance(_valid_to, Unset):
            valid_to = UNSET
        else:
            valid_to = isoparse(_valid_to)

        service_list_item_t = cls(
            controller_schema=controller_schema,
            href=href,
            id=id,
            description=description,
            name=name,
            tags=tags,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        service_list_item_t.additional_properties = d
        return service_list_item_t

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
