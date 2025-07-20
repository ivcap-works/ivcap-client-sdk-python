from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_t import ParameterT


T = TypeVar("T", bound="OrderRequestT")


@_attrs_define
class OrderRequestT:
    """
    Example:
        {'name': 'Fire risk for Lot2', 'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold',
            'value': '10'}], 'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'service':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}

    Attributes:
        parameters (list['ParameterT']): Service parameters Example: [{'name': 'region', 'value': 'Upper Valley'},
            {'name': 'threshold', 'value': '10'}].
        service (str): Reference to service requested Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        tags (Union[Unset, list[str]]): Optional customer provided tags Example: ['tag1', 'tag2'].
    """

    parameters: list["ParameterT"]
    service: str
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        service = self.service

        name = self.name

        policy = self.policy

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameters": parameters,
                "service": service,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.parameter_t import ParameterT

        d = src_dict.copy()
        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        service = d.pop("service")

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        order_request_t = cls(
            parameters=parameters,
            service=service,
            name=name,
            policy=policy,
            tags=tags,
        )

        order_request_t.additional_properties = d
        return order_request_t

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
