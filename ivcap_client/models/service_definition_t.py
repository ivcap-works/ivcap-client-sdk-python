from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.parameter_def_t import ParameterDefT


T = TypeVar("T", bound="ServiceDefinitionT")


@_attrs_define
class ServiceDefinitionT:
    """
    Example:
        {'controller': [{'$schema': 'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'],
            'image': 'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits': {'cpu':
            '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m', 'ephemeral-storage': '1Gi',
            'memory': '1Gi'}}}], 'controller-schema': 'urn:ivcap:schema.service.argo.1', 'description': 'This service ...',
            'id': 'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'name': 'Fire risk for Lot2', 'parameters':
            [{'description': 'The name of the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type':
            'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'tags': ['tag1', 'tag2']}

    Attributes:
        controller (File): controller definition Example: [{'$schema': 'urn:ivcap:schema.service.rest.1', 'command':
            ['python', '/app/tool-service.py'], 'image': 'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz',
            'resources': {'limits': {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu':
            '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}].
        controller_schema (str): type of controller used for this service Example: urn:ivcap:schema.service.argo.1.
        description (str): More detailed description of the service Example: This service ....
        id (str): ID Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        parameters (list['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        policy (str): Reference to policy used Example: urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        tags (Union[Unset, list[str]]): Optional tags defined for service to help in categorising them Example: ['tag1',
            'tag2'].
    """

    controller: File
    controller_schema: str
    description: str
    id: str
    parameters: list["ParameterDefT"]
    policy: str
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        controller = self.controller.to_tuple()

        controller_schema = self.controller_schema

        description = self.description

        id = self.id

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        policy = self.policy

        name = self.name

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "controller": controller,
                "controller-schema": controller_schema,
                "description": description,
                "id": id,
                "parameters": parameters,
                "policy": policy,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.parameter_def_t import ParameterDefT

        d = src_dict.copy()
        controller = File(payload=BytesIO(d.pop("controller")))

        controller_schema = d.pop("controller-schema")

        description = d.pop("description")

        id = d.pop("id")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterDefT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        policy = d.pop("policy")

        name = d.pop("name", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        service_definition_t = cls(
            controller=controller,
            controller_schema=controller_schema,
            description=description,
            id=id,
            parameters=parameters,
            policy=policy,
            name=name,
            tags=tags,
        )

        service_definition_t.additional_properties = d
        return service_definition_t

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
