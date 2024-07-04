from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_def_t import ParameterDefT
    from ..models.reference_t import ReferenceT
    from ..models.workflow_t import WorkflowT


T = TypeVar("T", bound="ServiceDefinitionT")


@_attrs_define
class ServiceDefinitionT:
    """
    Example:
        {'banner': 'http://ondricka.info/maci', 'description': 'This service ...', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label': 'Region Name', 'name':
            'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit':
            'm'}], 'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Autem
            corporis omnis ullam ipsum.', 'uri': 'http://smitham.net/adela.koelpin'}, {'title': 'Autem corporis omnis ullam
            ipsum.', 'uri': 'http://smitham.net/adela.koelpin'}, {'title': 'Autem corporis omnis ullam ipsum.', 'uri':
            'http://smitham.net/adela.koelpin'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Alias ab amet accusamus
            assumenda nobis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request':
            '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-tesla-t4',
            'image': 'alpine', 'image-pull-policy': 'Atque exercitationem nobis perspiciatis voluptate quia nihil.',
            'memory': {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type': 'basic'}}

    Attributes:
        description (str): More detailed description of the service Example: This service ....
        parameters (List['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        workflow (WorkflowT): Defines the workflow to use to execute this service. Currently supported 'types' are
            'basic'
                    and 'argo'. In case of 'basic', use the 'basic' element for further parameters. In the current implementation
                    'opts' is expected to contain the same schema as 'basic' Example: {'argo': 'Magni iste.', 'basic': {'command':
            ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-storage': {'limit':
            '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-
            policy': 'Atque exercitationem nobis perspiciatis voluptate quia nihil.', 'memory': {'limit': '100Mi',
            'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type': 'basic'}.
        banner (Union[Unset, str]): Link to banner image optionally used for this service Example:
            http://gerhold.biz/myrna.mitchell.
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        references (Union[Unset, List['ReferenceT']]): Reference to account revenues for this service should be credited
            to Example: [{'title': 'Autem corporis omnis ullam ipsum.', 'uri': 'http://smitham.net/adela.koelpin'},
            {'title': 'Autem corporis omnis ullam ipsum.', 'uri': 'http://smitham.net/adela.koelpin'}].
        tags (Union[Unset, List[str]]): Optional provider provided tags Example: ['tag1', 'tag2'].
    """

    description: str
    parameters: List["ParameterDefT"]
    workflow: "WorkflowT"
    banner: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    references: Union[Unset, List["ReferenceT"]] = UNSET
    tags: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        workflow = self.workflow.to_dict()

        banner = self.banner

        name = self.name

        policy = self.policy

        references: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.references, Unset):
            references = []
            for references_item_data in self.references:
                references_item = references_item_data.to_dict()
                references.append(references_item)

        tags: Union[Unset, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "parameters": parameters,
                "workflow": workflow,
            }
        )
        if banner is not UNSET:
            field_dict["banner"] = banner
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if references is not UNSET:
            field_dict["references"] = references
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.parameter_def_t import ParameterDefT
        from ..models.reference_t import ReferenceT
        from ..models.workflow_t import WorkflowT

        d = src_dict.copy()
        description = d.pop("description")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterDefT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        workflow = WorkflowT.from_dict(d.pop("workflow"))

        banner = d.pop("banner", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        references = []
        _references = d.pop("references", UNSET)
        for references_item_data in _references or []:
            references_item = ReferenceT.from_dict(references_item_data)

            references.append(references_item)

        tags = cast(List[str], d.pop("tags", UNSET))

        service_definition_t = cls(
            description=description,
            parameters=parameters,
            workflow=workflow,
            banner=banner,
            name=name,
            policy=policy,
            references=references,
            tags=tags,
        )

        service_definition_t.additional_properties = d
        return service_definition_t

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
