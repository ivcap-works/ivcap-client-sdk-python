import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.order_list_item_status import OrderListItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrderListItem")


@_attrs_define
class OrderListItem:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'finished-at':
            '1996-12-19T16:39:57-08:00', 'href': 'https://api.ivcap.net/1/orders/...', 'id':
            'urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2', 'ordered-at':
            '1996-12-19T16:39:57-08:00', 'service': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'started-at':
            '1996-12-19T16:39:57-08:00', 'status': 'executing'}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        href (str):  Example: https://api.ivcap.net/1/orders/....
        id (str): ID Example: urn:ivcap:order:123e4567-e89b-12d3-a456-426614174000.
        service (str): Reference to service requested Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        status (OrderListItemStatus): Order status Example: pending.
        finished_at (Union[Unset, datetime.datetime]): DateTime order processing finished Example:
            1996-12-19T16:39:57-08:00.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        ordered_at (Union[Unset, datetime.datetime]): DateTime order was placed Example: 1996-12-19T16:39:57-08:00.
        started_at (Union[Unset, datetime.datetime]): DateTime order processing started Example:
            1996-12-19T16:39:57-08:00.
    """

    account: str
    href: str
    id: str
    service: str
    status: OrderListItemStatus
    finished_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    ordered_at: Union[Unset, datetime.datetime] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        href = self.href

        id = self.id

        service = self.service

        status = self.status.value

        finished_at: Union[Unset, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat()

        name = self.name

        ordered_at: Union[Unset, str] = UNSET
        if not isinstance(self.ordered_at, Unset):
            ordered_at = self.ordered_at.isoformat()

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
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
        if ordered_at is not UNSET:
            field_dict["ordered-at"] = ordered_at
        if started_at is not UNSET:
            field_dict["started-at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        account = d.pop("account")

        href = d.pop("href")

        id = d.pop("id")

        service = d.pop("service")

        status = OrderListItemStatus(d.pop("status"))

        _finished_at = d.pop("finished-at", UNSET)
        finished_at: Union[Unset, datetime.datetime]
        if isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        name = d.pop("name", UNSET)

        _ordered_at = d.pop("ordered-at", UNSET)
        ordered_at: Union[Unset, datetime.datetime]
        if isinstance(_ordered_at, Unset):
            ordered_at = UNSET
        else:
            ordered_at = isoparse(_ordered_at)

        _started_at = d.pop("started-at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        order_list_item = cls(
            account=account,
            href=href,
            id=id,
            service=service,
            status=status,
            finished_at=finished_at,
            name=name,
            ordered_at=ordered_at,
            started_at=started_at,
        )

        order_list_item.additional_properties = d
        return order_list_item

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
