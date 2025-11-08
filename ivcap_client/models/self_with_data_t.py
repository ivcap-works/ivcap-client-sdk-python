from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.described_by_t import DescribedByT


T = TypeVar("T", bound="SelfWithDataT")


@_attrs_define
class SelfWithDataT:
    """
    Example:
        {'data': 'Assumenda voluptatem cupiditate doloribus.', 'describedBy': {'href': 'https://api.com/swagger/...',
            'type': 'application/openapi3+json'}, 'self': 'Qui et in.'}

    Attributes:
        data (Union[Unset, str]):  Example: Sed neque..
        described_by (Union[Unset, DescribedByT]):  Example: {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}.
        self_ (Union[Unset, str]):  Example: Incidunt reprehenderit quaerat laudantium quo aut qui..
    """

    data: Union[Unset, str] = UNSET
    described_by: Union[Unset, "DescribedByT"] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data

        described_by: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.described_by, Unset):
            described_by = self.described_by.to_dict()

        self_ = self.self_

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
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
