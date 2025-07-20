import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_list_item_status import JobListItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="JobListItem")


@_attrs_define
class JobListItem:
    """
    Example:
        {'finished-at': '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/services/...', 'id':
            'urn:ivcap:job:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for region', 'order':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at': '1996-12-19T16:39:57-08:00', 'status':
            'executing'}

    Attributes:
        href (str):  Example: https://api.ivcap.net/1/services/....
        id (str): ID Example: urn:ivcap:job:123e4567-e89b-12d3-a456-426614174000.
        service (str): Reference to service requested Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        status (JobListItemStatus): Job status Example: failed.
        finished_at (Union[Unset, datetime.datetime]): DateTime job processing finished Example:
            1996-12-19T16:39:57-08:00.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for region.
        order (Union[Unset, str]): Reference to order Example: urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        started_at (Union[Unset, datetime.datetime]): DateTime job processing started Example:
            1996-12-19T16:39:57-08:00.
    """

    href: str
    id: str
    service: str
    status: JobListItemStatus
    finished_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    order: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        id = self.id

        service = self.service

        status = self.status.value

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        name = self.name

        order = self.order

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "href": href,
                "id": id,
                "service": service,
                "status": status,
            }
        )
        if finished_at is not UNSET:
            field_dict["finished-at"] = finished_at
        if name is not UNSET:
            field_dict["name"] = name
        if order is not UNSET:
            field_dict["order"] = order
        if started_at is not UNSET:
            field_dict["started-at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        href = d.pop("href")

        id = d.pop("id")

        service = d.pop("service")

        status = JobListItemStatus(d.pop("status"))

        _finished_at = d.pop("finished-at", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        name = d.pop("name", UNSET)

        order = d.pop("order", UNSET)

        _started_at = d.pop("started-at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        job_list_item = cls(
            href=href,
            id=id,
            service=service,
            status=status,
            finished_at=finished_at,
            name=name,
            order=order,
            started_at=started_at,
        )

        job_list_item.additional_properties = d
        return job_list_item

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
