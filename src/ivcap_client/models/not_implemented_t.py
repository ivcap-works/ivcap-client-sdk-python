from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="NotImplementedT")


@attr.s(auto_attribs=True)
class NotImplementedT:
    """Method is not yet implemented

    Example:
        {'message': 'Mollitia velit.'}

    Attributes:
        message (str): Information message Default: 'Method not implemented'. Example: Quos inventore velit..
    """

    message: str = "Method not implemented"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        not_implemented_t = cls(
            message=message,
        )

        not_implemented_t.additional_properties = d
        return not_implemented_t

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
