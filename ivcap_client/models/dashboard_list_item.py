from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DashboardListItem")


@_attrs_define
class DashboardListItem:
    """
    Example:
        {'id': 3, 'title': 'Kubernetes Cluster Monitoring', 'uid': 'aeawr2d4xw7pcc', 'url': '/d/aeawr2d4xw7pcc'}

    Attributes:
        id (int): dashboard id Example: 3.
        title (str): Dashboard title Example: Kubernetes Cluster Monitoring.
        uid (str): dashboard uid Example: aeawr2d4xw7pcc.
        url (str): Dashboard url Example: /d/aeawr2d4xw7pcc.
    """

    id: int
    title: str
    uid: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        uid = self.uid

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "uid": uid,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        uid = d.pop("uid")

        url = d.pop("url")

        dashboard_list_item = cls(
            id=id,
            title=title,
            uid=uid,
            url=url,
        )

        dashboard_list_item.additional_properties = d
        return dashboard_list_item

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
