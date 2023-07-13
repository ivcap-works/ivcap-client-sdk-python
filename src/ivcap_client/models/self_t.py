from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.described_by_t import DescribedByT


T = TypeVar("T", bound="SelfT")


@attr.s(auto_attribs=True)
class SelfT:
    """
    Example:
        {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Corrupti
            laborum qui incidunt.'}

    Attributes:
        described_by (Union[Unset, DescribedByT]):  Example: {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}.
        self_ (Union[Unset, str]):  Example: Non et nemo excepturi ex..
    """

    described_by: Union[Unset, "DescribedByT"] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        described_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.described_by, Unset):
            described_by = self.described_by.to_dict()

        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if described_by is not UNSET:
            field_dict["describedBy"] = described_by
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.described_by_t import DescribedByT

        d = src_dict.copy()
        _described_by = d.pop("describedBy", UNSET)
        described_by: Union[Unset, DescribedByT]
        if isinstance(_described_by, Unset):
            described_by = UNSET
        else:
            described_by = DescribedByT.from_dict(_described_by)

        self_ = d.pop("self", UNSET)

        self_t = cls(
            described_by=described_by,
            self_=self_,
        )

        self_t.additional_properties = d
        return self_t

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
