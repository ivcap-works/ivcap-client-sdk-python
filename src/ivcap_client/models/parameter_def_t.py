from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

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
        {'constant': True, 'default': 'Natus quaerat veritatis at aut sed.', 'description': 'Omnis dicta incidunt
            impedit necessitatibus.', 'label': 'Quidem eum.', 'name': 'Quia molestiae id magni.', 'optional': True,
            'options': [{'description': 'Vel sequi repudiandae doloremque sit doloribus optio.', 'value': 'Blanditiis ullam
            nemo necessitatibus.'}, {'description': 'Vel sequi repudiandae doloremque sit doloribus optio.', 'value':
            'Blanditiis ullam nemo necessitatibus.'}, {'description': 'Vel sequi repudiandae doloremque sit doloribus
            optio.', 'value': 'Blanditiis ullam nemo necessitatibus.'}], 'type': 'Molestiae quo.', 'unary': True, 'unit':
            'Accusantium suscipit nisi labore.'}

    Attributes:
        description (str):  Example: Optio minima et quisquam ipsum rem dolore..
        name (str):  Example: Et vel beatae..
        type (str):  Example: Quibusdam nemo maxime qui expedita quasi natus..
        constant (Union[Unset, bool]):  Example: True.
        default (Union[Unset, str]):  Example: Ex dolores culpa vero asperiores aliquid..
        label (Union[Unset, str]):  Example: Quis voluptate quis ipsa repudiandae quidem eos..
        optional (Union[Unset, bool]):
        options (Union[Unset, List['ParameterOptT']]):  Example: [{'description': 'Vel sequi repudiandae doloremque sit
            doloribus optio.', 'value': 'Blanditiis ullam nemo necessitatibus.'}, {'description': 'Vel sequi repudiandae
            doloremque sit doloribus optio.', 'value': 'Blanditiis ullam nemo necessitatibus.'}, {'description': 'Vel sequi
            repudiandae doloremque sit doloribus optio.', 'value': 'Blanditiis ullam nemo necessitatibus.'}].
        unary (Union[Unset, bool]):  Example: True.
        unit (Union[Unset, str]):  Example: Qui est nostrum..
    """

    description: str
    name: str
    type: str
    constant: Union[Unset, bool] = UNSET
    default: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    optional: Union[Unset, bool] = UNSET
    options: Union[Unset, List["ParameterOptT"]] = UNSET
    unary: Union[Unset, bool] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        name = self.name

        type = self.type

        constant = self.constant

        default = self.default

        label = self.label

        optional = self.optional

        options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()
                options.append(options_item)

        unary = self.unary

        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "name": name,
                "type": type,
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
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_opt_t import ParameterOptT

        d = src_dict.copy()
        description = d.pop("description")

        name = d.pop("name")

        type = d.pop("type")

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
            type=type,
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
