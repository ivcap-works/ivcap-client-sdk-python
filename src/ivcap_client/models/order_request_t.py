from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_t import ParameterT


T = TypeVar("T", bound="OrderRequestT")


@define
class OrderRequestT:
    """
    Example:
        {'accountID': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2',
            'parameters': [{'name': 'region', 'value': 'Upper Valley'}, {'name': 'threshold', 'value': 10}], 'policyID':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'serviceID':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        account_id (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        parameters (List['ParameterT']): Service parameters Example: [{'name': 'region', 'value': 'Upper Valley'},
            {'name': 'threshold', 'value': 10}].
        service_id (str): Reference to service requested Example:
            urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        name (Union[Unset, str]): Optional customer provided name Example: Fire risk for Lot2.
        policy_id (Union[Unset, str]): Policy to control access to record an all generated artifacts Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
    """

    account_id: str
    parameters: List["ParameterT"]
    service_id: str
    name: Union[Unset, str] = UNSET
    policy_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account_id = self.account_id
        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()

            parameters.append(parameters_item)

        service_id = self.service_id
        name = self.name
        policy_id = self.policy_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accountID": account_id,
                "parameters": parameters,
                "serviceID": service_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if policy_id is not UNSET:
            field_dict["policyID"] = policy_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_t import ParameterT

        d = src_dict.copy()
        account_id = d.pop("accountID")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        service_id = d.pop("serviceID")

        name = d.pop("name", UNSET)

        policy_id = d.pop("policyID", UNSET)

        order_request_t = cls(
            account_id=account_id,
            parameters=parameters,
            service_id=service_id,
            name=name,
            policy_id=policy_id,
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
