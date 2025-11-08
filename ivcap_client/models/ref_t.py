from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_t import SelfT


T = TypeVar("T", bound="RefT")


@_attrs_define
class RefT:
    """
    Example:
        {'id': 'http://lakin.info/donnell', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Sed debitis ut culpa.'}}

    Attributes:
        id (Union[Unset, str]):  Example: http://schmeler.biz/liam_krajcik.
        links (Union[Unset, SelfT]):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Perspiciatis quidem.'}.
    """

    id: Union[Unset, str] = UNSET
    links: Union[Unset, "SelfT"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        links: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.self_t import SelfT

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _links = d.pop("links", UNSET)
        links: Union[Unset, SelfT]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = SelfT.from_dict(_links)

        ref_t = cls(
            id=id,
            links=links,
        )

        ref_t.additional_properties = d
        return ref_t

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
