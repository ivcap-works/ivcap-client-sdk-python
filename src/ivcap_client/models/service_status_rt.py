from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define, field

from ..models.service_status_rt_status import ServiceStatusRTStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_def_t import ParameterDefT
    from ..models.parameter_t import ParameterT
    from ..models.ref_t import RefT
    from ..models.self_t import SelfT


T = TypeVar("T", bound="ServiceStatusRT")


@define
class ServiceStatusRT:
    """
    Example:
        {'account': {'id': 'http://beahan.net/laurie', 'links': {'describedBy': {'href': 'https://api.com/swagger/...',
            'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}, 'description': 'This service ...', 'id':
            'service:acme:oracle', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Omnis cum odit.'}, 'metadata': [{'name': 'Recusandae quis.', 'value':
            'Dignissimos qui expedita quia deserunt veritatis.'}, {'name': 'Recusandae quis.', 'value': 'Dignissimos qui
            expedita quia deserunt veritatis.'}], 'name': 'Fire risk for Lot2', 'parameters': [{'description': 'The name of
            the region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}], 'provider': {'id':
            'http://beahan.net/laurie', 'links': {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}, 'provider-ref': 'service_foo', 'status': 'inactive',
            'tags': ['tag1', 'tag2']}

    Attributes:
        id (str): Service ID Example: service:acme:oracle.
        links (SelfT):  Example: {'describedBy': {'href': 'https://api.com/swagger/...', 'type':
            'application/openapi3+json'}, 'self': 'At qui.'}.
        parameters (List['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        account (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy': {'href':
            'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        description (Union[Unset, str]): More detailed description of the service Example: This service ....
        metadata (Union[Unset, List['ParameterT']]): Optional provider provided meta tags Example: [{'name': 'Recusandae
            quis.', 'value': 'Dignissimos qui expedita quia deserunt veritatis.'}, {'name': 'Recusandae quis.', 'value':
            'Dignissimos qui expedita quia deserunt veritatis.'}, {'name': 'Recusandae quis.', 'value': 'Dignissimos qui
            expedita quia deserunt veritatis.'}].
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        provider (Union[Unset, RefT]):  Example: {'id': 'http://lind.org/ruthe.kemmer', 'links': {'describedBy':
            {'href': 'https://api.com/swagger/...', 'type': 'application/openapi3+json'}, 'self': 'Omnis cum odit.'}}.
        provider_ref (Union[Unset, str]): Provider provided ID. Needs to be a single string with punctuations allowed.
            Might have been changed Example: service_foo.
        status (Union[Unset, ServiceStatusRTStatus]): Service status Example: active.
        tags (Union[Unset, List[str]]): Optional provider provided tags Example: ['tag1', 'tag2'].
    """

    id: str
    links: "SelfT"
    parameters: List["ParameterDefT"]
    account: Union[Unset, "RefT"] = UNSET
    description: Union[Unset, str] = UNSET
    metadata: Union[Unset, List["ParameterT"]] = UNSET
    name: Union[Unset, str] = UNSET
    provider: Union[Unset, "RefT"] = UNSET
    provider_ref: Union[Unset, str] = UNSET
    status: Union[Unset, ServiceStatusRTStatus] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        links = self.links.to_dict()

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()

            parameters.append(parameters_item)

        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        description = self.description
        metadata: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = []
            for metadata_item_data in self.metadata:
                metadata_item = metadata_item_data.to_dict()

                metadata.append(metadata_item)

        name = self.name
        provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        provider_ref = self.provider_ref
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "links": links,
                "parameters": parameters,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if provider is not UNSET:
            field_dict["provider"] = provider
        if provider_ref is not UNSET:
            field_dict["provider-ref"] = provider_ref
        if status is not UNSET:
            field_dict["status"] = status
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_def_t import ParameterDefT
        from ..models.parameter_t import ParameterT
        from ..models.ref_t import RefT
        from ..models.self_t import SelfT

        d = src_dict.copy()
        id = d.pop("id")

        links = SelfT.from_dict(d.pop("links"))

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterDefT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        _account = d.pop("account", UNSET)
        account: Union[Unset, RefT]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = RefT.from_dict(_account)

        description = d.pop("description", UNSET)

        metadata = []
        _metadata = d.pop("metadata", UNSET)
        for metadata_item_data in _metadata or []:
            metadata_item = ParameterT.from_dict(metadata_item_data)

            metadata.append(metadata_item)

        name = d.pop("name", UNSET)

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, RefT]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = RefT.from_dict(_provider)

        provider_ref = d.pop("provider-ref", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ServiceStatusRTStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ServiceStatusRTStatus(_status)

        tags = cast(List[str], d.pop("tags", UNSET))

        service_status_rt = cls(
            id=id,
            links=links,
            parameters=parameters,
            account=account,
            description=description,
            metadata=metadata,
            name=name,
            provider=provider,
            provider_ref=provider_ref,
            status=status,
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
