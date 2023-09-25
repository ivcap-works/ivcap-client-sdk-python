from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_t import SelfT


T = TypeVar("T", bound="CreateServiceResponseBodyTiny")


@define
class CreateServiceResponseBodyTiny:
    """create_service_response_body result type (tiny view)

    Example:
        {'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self':
            'Omnis cum odit.'}, 'name': 'Fire risk for Lot2'}

    Attributes:
        links (SelfT):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'At qui.'}.
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
    """

    links: "SelfT"
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        links = self.links.to_dict()

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "links": links,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.self_t import SelfT

        d = src_dict.copy()
        links = SelfT.from_dict(d.pop("links"))

        name = d.pop("name", UNSET)

        create_service_response_body_tiny = cls(
            links=links,
            name=name,
        )

        create_service_response_body_tiny.additional_properties = d
        return create_service_response_body_tiny

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
