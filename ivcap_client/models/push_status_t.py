from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PushStatusT")


@_attrs_define
class PushStatusT:
    """
    Example:
        {'message': 'Voluptas ut aut placeat autem aut.', 'status': 'Consectetur cumque debitis.'}

    Attributes:
        message (str): Message Example: Quo qui..
        status (str): Push status Example: Blanditiis nesciunt at qui suscipit..
    """

    message: str
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        status = d.pop("status")

        push_status_t = cls(
            message=message,
            status=status,
        )

        push_status_t.additional_properties = d
        return push_status_t

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
