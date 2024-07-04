from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.service_status_rt_status import ServiceStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.parameter_def_t import ParameterDefT


T = TypeVar("T", bound="ServiceStatusRT")


@_attrs_define
class ServiceStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The name of the region as
            according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month
            threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'status': 'inactive', 'tags': ['tag1', 'tag2']}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        id (str): ID Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        links (List['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        parameters (List['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        status (ServiceStatusRTStatus): Service status Example: active.
        description (Union[Unset, str]): More detailed description of the service Example: This service ....
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        tags (Union[Unset, List[str]]): Optional provider provided tags Example: ['tag1', 'tag2'].
    """

    account: str
    id: str
    links: List["LinkT"]
    parameters: List["ParameterDefT"]
    status: ServiceStatusRTStatus
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        account = self.account

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        status = self.status.value

        description = self.description

        name = self.name

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "id": id,
                "links": links,
                "parameters": parameters,
                "status": status,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.parameter_def_t import ParameterDefT

        d = src_dict.copy()
        account = d.pop("account")

        id = d.pop("id")

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = LinkT.from_dict(links_item_data)

            links.append(links_item)

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterDefT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        status = ServiceStatusRTStatus(d.pop("status"))

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        service_status_rt = cls(
            account=account,
            id=id,
            links=links,
            parameters=parameters,
            status=status,
            description=description,
            name=name,
            tags=tags,
        )

        service_status_rt.additional_properties = d
        return service_status_rt

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
