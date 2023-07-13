from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceMemoryT")


@attr.s(auto_attribs=True)
class ResourceMemoryT:
    """See
    and https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/ for units

        Example:
            {'limit': 'Aut odit dolorum nulla quo.', 'request': 'Est esse voluptas consectetur quia.'}

        Attributes:
            limit (Union[Unset, str]): minimal requirements [system limit] Example: Molestiae et ex hic aut dicta dolorem..
            request (Union[Unset, str]): minimal requirements [0] Example: Voluptas odit..
    """

    limit: Union[Unset, str] = UNSET
    request: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        limit = self.limit
        request = self.request

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if request is not UNSET:
            field_dict["request"] = request

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        limit = d.pop("limit", UNSET)

        request = d.pop("request", UNSET)

        resource_memory_t = cls(
            limit=limit,
            request=request,
        )

        resource_memory_t.additional_properties = d
        return resource_memory_t

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
