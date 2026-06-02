from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.self_with_data_t import SelfWithDataT


T = TypeVar("T", bound="ProductT")


@_attrs_define
class ProductT:
    """
    Example:
        {'etag': 'Est autem sit quibusdam illo dignissimos.', 'id': 'Pariatur quis repellendus.', 'links': {'data':
            'Rerum dolor eum vitae esse id.', 'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Expedita ea.'}, 'mime-type': 'Dignissimos impedit accusamus aut sint
            et.', 'name': 'Nulla repellendus eum.', 'size': 892074325640234524, 'status': 'Autem qui maxime hic soluta
            quis.'}

    Attributes:
        etag (str | Unset):  Example: Ut quasi minus et ad eius commodi..
        id (str | Unset):  Example: Assumenda dolore..
        links (SelfWithDataT | Unset):  Example: {'data': 'Assumenda voluptatem cupiditate doloribus.', 'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Qui et in.'}.
        mime_type (str | Unset):  Example: Placeat tenetur qui libero et iusto et..
        name (str | Unset):  Example: Assumenda dolorem eveniet illo repellendus atque ad..
        size (int | Unset):  Example: 1903424111964933358.
        status (str | Unset):  Example: Adipisci atque itaque aut nostrum maiores..
    """

    etag: str | Unset = UNSET
    id: str | Unset = UNSET
    links: SelfWithDataT | Unset = UNSET
    mime_type: str | Unset = UNSET
    name: str | Unset = UNSET
    size: int | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        etag = self.etag

        id = self.id

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        mime_type = self.mime_type

        name = self.name

        size = self.size

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if etag is not UNSET:
            field_dict["etag"] = etag
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
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.self_with_data_t import SelfWithDataT

        d = dict(src_dict)
        etag = d.pop("etag", UNSET)

        id = d.pop("id", UNSET)

        _links = d.pop("links", UNSET)
        links: SelfWithDataT | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = SelfWithDataT.from_dict(_links)

        mime_type = d.pop("mime-type", UNSET)

        name = d.pop("name", UNSET)

        size = d.pop("size", UNSET)

        status = d.pop("status", UNSET)

        product_t = cls(
            etag=etag,
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
