from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReferenceT")


@define
class ReferenceT:
    """
    Example:
        {'title': 'Beatae incidunt voluptas sequi debitis est quis.', 'uri': 'http://rowejakubowski.biz/jason.bosco'}

    Attributes:
        title (Union[Unset, str]): Title of reference document Example: Et a..
        uri (Union[Unset, str]): Link to document Example: http://ziemann.biz/lucienne.
    """

    title: Union[Unset, str] = UNSET
    uri: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        uri = self.uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if uri is not UNSET:
            field_dict["uri"] = uri

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        uri = d.pop("uri", UNSET)

        reference_t = cls(
            title=title,
            uri=uri,
        )

        reference_t.additional_properties = d
        return reference_t

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
