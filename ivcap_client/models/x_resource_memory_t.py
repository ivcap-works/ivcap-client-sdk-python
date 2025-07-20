from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="XResourceMemoryT")


@_attrs_define
class XResourceMemoryT:
    """See https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes for
    units

        Example:
            {'limit': 'Iste nemo et harum hic qui voluptas.', 'request': 'Minima ut ipsam.'}

        Attributes:
            limit (Union[Unset, str]): minimal requirements [system limit] Example: At qui..
            request (Union[Unset, str]): minimal requirements [0] Example: Alias velit adipisci..
    """

    limit: Union[Unset, str] = UNSET
    request: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        request = self.request

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if request is not UNSET:
            field_dict["request"] = request

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        limit = d.pop("limit", UNSET)

        request = d.pop("request", UNSET)

        x_resource_memory_t = cls(
            limit=limit,
            request=request,
        )

        x_resource_memory_t.additional_properties = d
        return x_resource_memory_t

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
