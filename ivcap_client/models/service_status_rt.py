import datetime
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.service_status_rt_status import ServiceStatusRTStatus
from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.link_t import LinkT
    from ..models.parameter_def_t import ParameterDefT


T = TypeVar("T", bound="ServiceStatusRT")


@_attrs_define
class ServiceStatusRT:
    """
    Example:
        {'account': 'urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000', 'controller': [{'$schema':
            'urn:ivcap:schema.service.rest.1', 'command': ['python', '/app/tool-service.py'], 'image': 'your-docker-
            image:latest', 'port': 8090, 'ready-url': '/_healtz', 'resources': {'limits': {'cpu': '500m', 'ephemeral-
            storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}],
            'controller-schema': 'urn:ivcap:schema.service.argo.1', 'description': 'This service ...', 'id':
            'urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000', 'links': [{'href': 'https://api.ivcap.net/1/....',
            'rel': 'self', 'type': 'application/json'}, {'href':
            'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel': 'describedBy', 'type':
            'application/json'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The name of the region as
            according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label': 'Rainfall/month
            threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'status': 'error', 'tags': ['tag1', 'tag2'], 'valid-
            from': '1996-12-19T16:39:57-08:00', 'valid-to': '1996-12-19T16:39:57-08:00'}

    Attributes:
        account (str): Reference to billable account Example: urn:ivcap:account:123e4567-e89b-12d3-a456-426614174000.
        controller (File): controller definition Example: [{'$schema': 'urn:ivcap:schema.service.rest.1', 'command':
            ['python', '/app/tool-service.py'], 'image': 'your-docker-image:latest', 'port': 8090, 'ready-url': '/_healtz',
            'resources': {'limits': {'cpu': '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}, 'requests': {'cpu':
            '500m', 'ephemeral-storage': '1Gi', 'memory': '1Gi'}}}].
        controller_schema (str): type of controller used for this service Example: urn:ivcap:schema.service.argo.1.
        description (str): More detailed description of the service Example: This service ....
        id (str): ID Example: urn:ivcap:service:123e4567-e89b-12d3-a456-426614174000.
        links (list['LinkT']):  Example: [{'href': 'https://api.ivcap.net/1/....', 'rel': 'self', 'type':
            'application/json'}, {'href': 'https://api.ivcap.net/1/openapi/openapi3.json#/components/schemas/user', 'rel':
            'describedBy', 'type': 'application/json'}].
        parameters (list['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        policy (str): Reference to policy used Example: urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        status (ServiceStatusRTStatus): Service status Example: error.
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        tags (Union[Unset, list[str]]): Optional tags defined for service to help in categorising them Example: ['tag1',
            'tag2'].
        valid_from (Union[Unset, datetime.datetime]): time this service has been available from Example:
            1996-12-19T16:39:57-08:00.
        valid_to (Union[Unset, datetime.datetime]): time this service has been available to Example:
            1996-12-19T16:39:57-08:00.
    """

    account: str
    controller: File
    controller_schema: str
    description: str
    id: str
    links: list["LinkT"]
    parameters: list["ParameterDefT"]
    policy: str
    status: ServiceStatusRTStatus
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    valid_from: Union[Unset, datetime.datetime] = UNSET
    valid_to: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        account = self.account

        controller = self.controller

        controller_schema = self.controller_schema

        description = self.description

        id = self.id

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        policy = self.policy

        status = self.status.value

        name = self.name

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        valid_from: Union[Unset, str] = UNSET
        if not isinstance(self.valid_from, Unset):
            valid_from = self.valid_from.isoformat()

        valid_to: Union[Unset, str] = UNSET
        if not isinstance(self.valid_to, Unset):
            valid_to = self.valid_to.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "account": account,
                "controller": controller,
                "controller-schema": controller_schema,
                "description": description,
                "id": id,
                "links": links,
                "parameters": parameters,
                "policy": policy,
                "status": status,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if valid_from is not UNSET:
            field_dict["valid-from"] = valid_from
        if valid_to is not UNSET:
            field_dict["valid-to"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.link_t import LinkT
        from ..models.parameter_def_t import ParameterDefT

        d = src_dict.copy()
        account = d.pop("account")

        controller = d.pop("controller")

        controller_schema = d.pop("controller-schema")

        description = d.pop("description")

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

        policy = d.pop("policy")

        status = ServiceStatusRTStatus(d.pop("status"))

        name = d.pop("name", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _valid_from = d.pop("valid-from", UNSET)
        valid_from: Union[Unset, datetime.datetime]
        if isinstance(_valid_from, Unset):
            valid_from = UNSET
        else:
            valid_from = isoparse(_valid_from)

        _valid_to = d.pop("valid-to", UNSET)
        valid_to: Union[Unset, datetime.datetime]
        if isinstance(_valid_to, Unset):
            valid_to = UNSET
        else:
            valid_to = isoparse(_valid_to)

        service_status_rt = cls(
            account=account,
            controller=controller,
            controller_schema=controller_schema,
            description=description,
            id=id,
            links=links,
            parameters=parameters,
            policy=policy,
            status=status,
            name=name,
            tags=tags,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        service_status_rt.additional_properties = d
        return service_status_rt

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
