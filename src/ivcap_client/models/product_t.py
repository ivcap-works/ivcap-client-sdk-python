from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_with_data_t import SelfWithDataT


T = TypeVar("T", bound="ProductT")


@define
class ProductT:
    """
    Example:
        {'id': 'Occaecati quia ut nostrum.', 'links': {'data': 'Quia ut pariatur.', 'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Sit cumque corrupti excepturi.'},
            'mime-type': 'Dolore voluptatem.', 'name': 'Suscipit officiis.', 'size': 4314372988661854938, 'status': 'Non
            occaecati sit.'}

    Attributes:
        id (Union[Unset, str]):  Example: Ex mollitia eum consequatur accusamus..
        links (Union[Unset, SelfWithDataT]):  Example: {'data': 'Assumenda aut quia commodi.', 'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Eos labore.'}.
        mime_type (Union[Unset, str]):  Example: Alias velit adipisci..
        name (Union[Unset, str]):  Example: Incidunt aperiam perspiciatis sit pariatur..
        size (Union[Unset, int]):  Example: 1667448502336650080.
        status (Union[Unset, str]):  Example: Voluptatem reiciendis similique repellendus et a..
    """

    id: Union[Unset, str] = UNSET
    links: Union[Unset, "SelfWithDataT"] = UNSET
    mime_type: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        links: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        mime_type = self.mime_type
        name = self.name
        size = self.size
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if links is not UNSET:
            field_dict["links"] = links
        if mime_type is not UNSET:
            field_dict["mime-type"] = mime_type
        if name is not UNSET:
            field_dict["name"] = name
        if size is not UNSET:
            field_dict["size"] = size
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.self_with_data_t import SelfWithDataT

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _links = d.pop("links", UNSET)
        links: Union[Unset, SelfWithDataT]
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = SelfWithDataT.from_dict(_links)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        status = d.pop("status", UNSET)

        product_t = cls(
            id=id,
            links=links,
            mime_type=mime_type,
            name=name,
            size=size,
            status=status,
        )

        product_t.additional_properties = d
        return product_t

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
