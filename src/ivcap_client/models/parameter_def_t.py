from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_opt_t import ParameterOptT


T = TypeVar("T", bound="ParameterDefT")


@define
class ParameterDefT:
    """
    Example:
        {'constant': False, 'default': 'Est nostrum.', 'description': 'Natus quaerat veritatis at aut sed.', 'label':
            'Quo est omnis dicta incidunt impedit.', 'name': 'Magni consequatur quidem eum velit.', 'optional': False,
            'options': [{'description': 'Ut fuga ea sapiente quo quo.', 'value': 'Repudiandae non corporis.'},
            {'description': 'Ut fuga ea sapiente quo quo.', 'value': 'Repudiandae non corporis.'}], 'type': 'Molestiae
            accusantium suscipit nisi labore omnis modi.', 'unit': 'Dolor natus nihil expedita voluptatum recusandae.'}

    Attributes:
        constant (Union[Unset, bool]):  Example: True.
        default (Union[Unset, str]):  Example: Animi inventore officiis repellendus ipsum quasi..
        description (Union[Unset, str]):  Example: Qui est nostrum..
        label (Union[Unset, str]):  Example: Quibusdam nemo maxime qui expedita quasi natus..
        name (Union[Unset, str]):  Example: Quis voluptate quis ipsa repudiandae quidem eos..
        optional (Union[Unset, bool]):  Example: True.
        options (Union[Unset, List['ParameterOptT']]):  Example: [{'description': 'Ut fuga ea sapiente quo quo.',
            'value': 'Repudiandae non corporis.'}, {'description': 'Ut fuga ea sapiente quo quo.', 'value': 'Repudiandae non
            corporis.'}, {'description': 'Ut fuga ea sapiente quo quo.', 'value': 'Repudiandae non corporis.'}].
        type (Union[Unset, str]):  Example: Optio minima et quisquam ipsum rem dolore..
        unit (Union[Unset, str]):  Example: Enim porro ex dolores culpa vero asperiores..
    """

    constant: Union[Unset, bool] = UNSET
    default: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    optional: Union[Unset, bool] = UNSET
    options: Union[Unset, List["ParameterOptT"]] = UNSET
    type: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constant = self.constant
        default = self.default
        description = self.description
        label = self.label
        name = self.name
        optional = self.optional
        options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.options, Unset):
            options = []
            for options_item_data in self.options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

        type = self.type
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constant is not UNSET:
            field_dict["constant"] = constant
        if default is not UNSET:
            field_dict["default"] = default
        if description is not UNSET:
            field_dict["description"] = description
        if label is not UNSET:
            field_dict["label"] = label
        if name is not UNSET:
            field_dict["name"] = name
        if optional is not UNSET:
            field_dict["optional"] = optional
        if options is not UNSET:
            field_dict["options"] = options
        if type is not UNSET:
            field_dict["type"] = type
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_opt_t import ParameterOptT

        d = src_dict.copy()
        constant = d.pop("constant", UNSET)

        default = d.pop("default", UNSET)

        description = d.pop("description", UNSET)

        label = d.pop("label", UNSET)

        name = d.pop("name", UNSET)

        optional = d.pop("optional", UNSET)

        options = []
        _options = d.pop("options", UNSET)
        for options_item_data in _options or []:
            options_item = ParameterOptT.from_dict(options_item_data)

            options.append(options_item)

        type = d.pop("type", UNSET)

        unit = d.pop("unit", UNSET)

        parameter_def_t = cls(
            constant=constant,
            default=default,
            description=description,
            label=label,
            name=name,
            optional=optional,
            options=options,
            type=type,
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
