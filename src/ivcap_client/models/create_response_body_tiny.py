from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..models.create_response_body_tiny_status import CreateResponseBodyTinyStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_t import SelfT


T = TypeVar("T", bound="CreateResponseBodyTiny")


@define
class CreateResponseBodyTiny:
    """CreateResponseBody result type (tiny view)

    Example:
        {'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self':
            'Ipsam deleniti magnam nihil et.'}, 'name': 'Fire risk for Lot2', 'status': 'pending'}

    Attributes:
        links (Union[Unset, SelfT]):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Consequatur adipisci.'}.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        status (Union[Unset, CreateResponseBodyTinyStatus]): Order status Example: unknown.
    """

    links: Union[Unset, "SelfT"] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, CreateResponseBodyTinyStatus] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        name = self.name
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if links is not UNSET:
            field_dict["links"] = links
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.self_t import SelfT

        d = src_dict.copy()
        _links = d.pop("links", UNSET)
        links: Union[Unset, SelfT]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = SelfT.from_dict(_links)

        name = d.pop("name", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, CreateResponseBodyTinyStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = CreateResponseBodyTinyStatus(_status)

        create_response_body_tiny = cls(
            links=links,
            name=name,
            status=status,
        )

        create_response_body_tiny.additional_properties = d
        return create_response_body_tiny

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
