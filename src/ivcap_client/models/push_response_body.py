from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PushResponseBody")


@_attrs_define
class PushResponseBody:
    """
    Example:
        {'digest': 'Tenetur ratione qui amet reiciendis debitis.'}

    Attributes:
        digest (Union[Unset, str]): uploaded image digest or tag Example: Error id et..
    """

    digest: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        digest = self.digest

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if digest is not UNSET:
            field_dict["digest"] = digest

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        digest = d.pop("digest", UNSET)

        push_response_body = cls(
            digest=digest,
        )

        push_response_body.additional_properties = d
        return push_response_body

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
