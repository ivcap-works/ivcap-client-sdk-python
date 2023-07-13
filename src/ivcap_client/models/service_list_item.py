from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ref_t import RefT
    from ..models.self_t import SelfT


T = TypeVar("T", bound="ServiceListItem")


@attr.s(auto_attribs=True)
class ServiceListItem:
    """
    Example:
        {'description': 'Some lengthy description of fire risk', 'id': 'service:acme:oracle', 'links': {'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis
            incidunt.'}, 'name': 'Fire risk for region', 'provider': {'id': 'http://gorczany.com/breanne.block', 'links':
            {'describedBy': {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis
            reiciendis incidunt.'}}}

    Attributes:
        links (SelfT):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Corrupti laborum qui incidunt.'}.
        description (Union[Unset, str]): Optional description of the service Example: Some lengthy description of fire
            risk.
        id (Union[Unset, str]): Service ID Example: service:acme:oracle.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for region.
        provider (Union[Unset, RefT]):  Example: {'id': 'http://dooley.name/marlee.mueller', 'links': {'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Officiis reiciendis
            incidunt.'}}.
    """

    links: "SelfT"
    description: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    provider: Union[Unset, "RefT"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        links = self.links.to_dict()

        description = self.description
        id = self.id
        name = self.name
        provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "links": links,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ref_t import RefT
        from ..models.self_t import SelfT

        d = src_dict.copy()
        links = SelfT.from_dict(d.pop("links"))

        description = d.pop("description", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, RefT]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = RefT.from_dict(_provider)

        service_list_item = cls(
            links=links,
            description=description,
            id=id,
            name=name,
            provider=provider,
        )

        service_list_item.additional_properties = d
        return service_list_item

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
