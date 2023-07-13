from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.described_by_t import DescribedByT


T = TypeVar("T", bound="SelfWithDataT")


@attr.s(auto_attribs=True)
class SelfWithDataT:
    """
    Example:
        {'data': 'Repellendus vel nulla repellendus eum neque autem.', 'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Minus et ad eius commodi non
            pariatur.'}

    Attributes:
        data (Union[Unset, str]):  Example: Et iusto et magni vitae ut..
        described_by (Union[Unset, DescribedByT]):  Example: {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}.
        self_ (Union[Unset, str]):  Example: Maiores deleniti placeat tenetur qui..
    """

    data: Union[Unset, str] = UNSET
    described_by: Union[Unset, "DescribedByT"] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data
        described_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.described_by, Unset):
            described_by = self.described_by.to_dict()

        self_ = self.self_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if described_by is not UNSET:
            field_dict["describedBy"] = described_by
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.described_by_t import DescribedByT

        d = src_dict.copy()
        data = d.pop("data", UNSET)

        _described_by = d.pop("describedBy", UNSET)
        described_by: Union[Unset, DescribedByT]
        if isinstance(_described_by, Unset):
            described_by = UNSET
        else:
            described_by = DescribedByT.from_dict(_described_by)

        self_ = d.pop("self", UNSET)

        self_with_data_t = cls(
            data=data,
            described_by=described_by,
            self_=self_,
        )

        self_with_data_t.additional_properties = d
        return self_with_data_t

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
