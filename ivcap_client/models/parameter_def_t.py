from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_opt_t import ParameterOptT


T = TypeVar("T", bound="ParameterDefT")


@_attrs_define
class ParameterDefT:
    """
    Example:
        {'constant': False, 'default': 'Ratione repudiandae et sed.', 'description': 'Dolor porro est inventore eius
            aperiam tempora.', 'label': 'Aperiam reiciendis earum minima laborum dicta dolorum.', 'name': 'Quis sunt libero
            et.', 'optional': True, 'options': [{'description': 'Quo fugiat non qui nihil voluptatem ea.', 'value': 'Beatae
            voluptatem reprehenderit enim nisi qui occaecati.'}, {'description': 'Quo fugiat non qui nihil voluptatem ea.',
            'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}, {'description': 'Quo fugiat non qui nihil
            voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}, {'description': 'Quo
            fugiat non qui nihil voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}],
            'type': 'Repellat doloremque.', 'unary': False, 'unit': 'Dolorem nemo.'}

    Attributes:
        description (str):  Example: Qui maiores reprehenderit fuga harum impedit..
        name (str):  Example: Omnis dolor dicta quo..
        type_ (str):  Example: Ex ut consequatur pariatur rerum est et..
        constant (bool | Unset):
        default (str | Unset):  Example: Id vel voluptas quis autem..
        label (str | Unset):  Example: Natus sit..
        optional (bool | Unset):
        options (list[ParameterOptT] | Unset):  Example: [{'description': 'Quo fugiat non qui nihil voluptatem ea.',
            'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}, {'description': 'Quo fugiat non qui nihil
            voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}].
        unary (bool | Unset):  Example: True.
        unit (str | Unset):  Example: Voluptatibus doloremque ea molestiae ratione commodi..
    """

    description: str
    name: str
    type_: str
    constant: bool | Unset = UNSET
    default: str | Unset = UNSET
    label: str | Unset = UNSET
    optional: bool | Unset = UNSET
    options: list[ParameterOptT] | Unset = UNSET
    unary: bool | Unset = UNSET
    unit: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        type_ = self.type_

        constant = self.constant

        default = self.default

        label = self.label

        optional = self.optional

        options: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        unary = self.unary

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "name": name,
                "type": type_,
            }
        )
        if constant is not UNSET:
            field_dict["constant"] = constant
        if default is not UNSET:
            field_dict["default"] = default
        if label is not UNSET:
            field_dict["label"] = label
        if optional is not UNSET:
            field_dict["optional"] = optional
        if options is not UNSET:
            field_dict["options"] = options
        if unary is not UNSET:
            field_dict["unary"] = unary
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parameter_opt_t import ParameterOptT

        d = dict(src_dict)
        description = d.pop("description")

        name = d.pop("name")

        type_ = d.pop("type")

        constant = d.pop("constant", UNSET)

        default = d.pop("default", UNSET)

        label = d.pop("label", UNSET)

        optional = d.pop("optional", UNSET)

        _options = d.pop("options", UNSET)
        options: list[ParameterOptT] | Unset = UNSET
        if _options is not UNSET:
            options = []
            for options_item_data in _options:
                options_item = ParameterOptT.from_dict(options_item_data)

                options.append(options_item)

        unary = d.pop("unary", UNSET)

        unit = d.pop("unit", UNSET)

        parameter_def_t = cls(
            description=description,
            name=name,
            type_=type_,
            constant=constant,
            default=default,
            label=label,
            optional=optional,
            options=options,
            unary=unary,
            unit=unit,
        )

        parameter_def_t.additional_properties = d
        return parameter_def_t

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
