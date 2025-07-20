from typing import TYPE_CHECKING, Any, TypeVar, Union

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
        {'constant': False, 'default': 'Mollitia velit.', 'description': 'Cumque consequatur at est.', 'label': 'Et nemo
            excepturi ex.', 'name': 'Facilis et cum.', 'optional': True, 'options': [{'description': 'Quo fugiat non qui
            nihil voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}, {'description':
            'Quo fugiat non qui nihil voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'},
            {'description': 'Quo fugiat non qui nihil voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi
            qui occaecati.'}], 'type': 'Corrupti laborum qui incidunt.', 'unary': True, 'unit': 'Praesentium eaque explicabo
            facilis quos.'}

    Attributes:
        description (str):  Example: Eius vel..
        name (str):  Example: Earum aliquid aut cum..
        type_ (str):  Example: Veniam sunt quibusdam dolores officiis reprehenderit..
        constant (Union[Unset, bool]):  Example: True.
        default (Union[Unset, str]):  Example: Consequuntur incidunt iste..
        label (Union[Unset, str]):  Example: Perferendis rerum explicabo consequatur..
        optional (Union[Unset, bool]):  Example: True.
        options (Union[Unset, list['ParameterOptT']]):  Example: [{'description': 'Quo fugiat non qui nihil voluptatem
            ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}, {'description': 'Quo fugiat non qui
            nihil voluptatem ea.', 'value': 'Beatae voluptatem reprehenderit enim nisi qui occaecati.'}].
        unary (Union[Unset, bool]):  Example: True.
        unit (Union[Unset, str]):  Example: Quaerat cupiditate quidem corporis..
    """

    description: str
    name: str
    type_: str
    constant: Union[Unset, bool] = UNSET
    default: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    optional: Union[Unset, bool] = UNSET
    options: Union[Unset, list["ParameterOptT"]] = UNSET
    unary: Union[Unset, bool] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        type_ = self.type_

        constant = self.constant

        default = self.default

        label = self.label

        optional = self.optional

        options: Union[Unset, list[dict[str, Any]]] = UNSET
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.parameter_opt_t import ParameterOptT

        d = src_dict.copy()
        description = d.pop("description")

        name = d.pop("name")

        type_ = d.pop("type")

        constant = d.pop("constant", UNSET)

        default = d.pop("default", UNSET)

        label = d.pop("label", UNSET)

        optional = d.pop("optional", UNSET)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
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
