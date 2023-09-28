from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_t import ParameterT


T = TypeVar("T", bound="OrderRequestT")


@define
class OrderRequestT:
    """
    Example:
        {'account-id': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value': '10'}], 'policy-id':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'service-id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}

    Attributes:
        parameters (List['ParameterT']): Service parameters Example: [{'name': 'region', 'value': 'Upper Valley'},
            {'name': 'threshold', 'value': '10'}].
        service_id (str): Reference to service requested Example:
            urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        account_id (Union[Unset, str]): Reference to billable account Example:
            urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        policy_id (Union[Unset, str]): Policy to control access to record an all generated artifacts Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        tags (Union[Unset, List[str]]): Optional customer provided tags Example: ['tag1', 'tag2'].
    """

    parameters: List["ParameterT"]
    service_id: str
    account_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy_id: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()

            parameters.append(parameters_item)

        service_id = self.service_id
        account_id = self.account_id
        name = self.name
        policy_id = self.policy_id
        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameters": parameters,
                "service-id": service_id,
            }
        )
        if account_id is not UNSET:
            field_dict["account-id"] = account_id
        if name is not UNSET:
            field_dict["name"] = name
        if policy_id is not UNSET:
            field_dict["policy-id"] = policy_id
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_t import ParameterT

        d = src_dict.copy()
        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        service_id = d.pop("service-id")

        account_id = d.pop("account-id", UNSET)

        name = d.pop("name", UNSET)

        policy_id = d.pop("policy-id", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        order_request_t = cls(
            parameters=parameters,
            service_id=service_id,
            account_id=account_id,
            name=name,
            policy_id=policy_id,
            tags=tags,
        )

        order_request_t.additional_properties = d
        return order_request_t

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
