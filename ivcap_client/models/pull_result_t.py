from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PullResultT")


@_attrs_define
class PullResultT:
    """
    Example:
        {'available': 3010281367937960212, 'total': 5416446213319858753}

    Attributes:
        available (int): available size in bytes of layer to read Example: 6177584026154757210.
        total (int): total size in bytes of layer Example: 3555598158531092331.
    """

    available: int
    total: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        available = self.available

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "available": available,
                "total": total,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        available = d.pop("available")

        total = d.pop("total")

        pull_result_t = cls(
            available=available,
            total=total,
        )

        pull_result_t.additional_properties = d
        return pull_result_t

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
