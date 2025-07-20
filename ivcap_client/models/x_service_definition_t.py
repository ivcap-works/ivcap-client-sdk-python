from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameter_def_t import ParameterDefT
    from ..models.x_reference_t import XReferenceT
    from ..models.x_workflow_t import XWorkflowT


T = TypeVar("T", bound="XServiceDefinitionT")


@_attrs_define
class XServiceDefinitionT:
    """
    Example:
        {'banner': 'http://leffler.info/herminia', 'description': 'This service ...', 'name': 'Fire risk for Lot2',
            'parameters': [{'description': 'The name of the region as according to ...', 'label': 'Region Name', 'name':
            'region', 'type': 'string'}, {'label': 'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit':
            'm'}], 'policy': 'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000', 'references': [{'title': 'Assumenda
            sit.', 'uri': 'http://stoltenberg.name/aletha.howell'}, {'title': 'Assumenda sit.', 'uri':
            'http://stoltenberg.name/aletha.howell'}, {'title': 'Assumenda sit.', 'uri':
            'http://stoltenberg.name/aletha.howell'}, {'title': 'Assumenda sit.', 'uri':
            'http://stoltenberg.name/aletha.howell'}], 'tags': ['tag1', 'tag2'], 'workflow': {'argo': 'Aut consequuntur
            occaecati sint et dolor.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m',
            'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
            'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Natus officia quae sed blanditiis vero.', 'memory':
            {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type': 'basic'}}

    Attributes:
        description (str): More detailed description of the service Example: This service ....
        parameters (list['ParameterDefT']): Service parameter definitions Example: [{'description': 'The name of the
            region as according to ...', 'label': 'Region Name', 'name': 'region', 'type': 'string'}, {'label':
            'Rainfall/month threshold', 'name': 'threshold', 'type': 'float', 'unit': 'm'}].
        workflow (XWorkflowT): Defines the workflow to use to execute this service. Currently supported 'types' are
            'basic'
                    and 'argo'. In case of 'basic', use the 'basic' element for further parameters. In the current implementation
                    'opts' is expected to contain the same schema as 'basic' Example: {'argo': 'Quia ut nostrum est suscipit.',
            'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-
            storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-tesla-t4', 'image': 'alpine',
            'image-pull-policy': 'Natus officia quae sed blanditiis vero.', 'memory': {'limit': '100Mi', 'request': '10Mi'},
            'shared-memory': '1Gi'}, 'type': 'basic'}.
        banner (Union[Unset, str]): Link to banner image optionally used for this service Example:
            http://stark.com/bruce.
        name (Union[Unset, str]): Optional provider provided name Example: Fire risk for Lot2.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
        references (Union[Unset, list['XReferenceT']]): Reference to account revenues for this service should be
            credited to Example: [{'title': 'Assumenda sit.', 'uri': 'http://stoltenberg.name/aletha.howell'}, {'title':
            'Assumenda sit.', 'uri': 'http://stoltenberg.name/aletha.howell'}, {'title': 'Assumenda sit.', 'uri':
            'http://stoltenberg.name/aletha.howell'}].
        tags (Union[Unset, list[str]]): Optional provider provided tags Example: ['tag1', 'tag2'].
    """

    description: str
    parameters: list["ParameterDefT"]
    workflow: "XWorkflowT"
    banner: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    references: Union[Unset, list["XReferenceT"]] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        parameters = []
        for parameters_item_data in self.parameters:
            parameters_item = parameters_item_data.to_dict()
            parameters.append(parameters_item)

        workflow = self.workflow.to_dict()

        banner = self.banner

        name = self.name

        policy = self.policy

        references: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.references, Unset):
            references = []
            for references_item_data in self.references:
                references_item = references_item_data.to_dict()
                references.append(references_item)

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.parameter_def_t import ParameterDefT
        from ..models.x_reference_t import XReferenceT
        from ..models.x_workflow_t import XWorkflowT

        d = src_dict.copy()
        description = d.pop("description")

        parameters = []
        _parameters = d.pop("parameters")
        for parameters_item_data in _parameters:
            parameters_item = ParameterDefT.from_dict(parameters_item_data)

            parameters.append(parameters_item)

        workflow = XWorkflowT.from_dict(d.pop("workflow"))

        banner = d.pop("banner", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        references = []
        _references = d.pop("references", UNSET)
        for references_item_data in _references or []:
            references_item = XReferenceT.from_dict(references_item_data)

            references.append(references_item)

        tags = cast(list[str], d.pop("tags", UNSET))

        x_service_definition_t = cls(
            description=description,
            parameters=parameters,
            workflow=workflow,
            banner=banner,
            name=name,
            policy=policy,
            references=references,
            tags=tags,
        )

        x_service_definition_t.additional_properties = d
        return x_service_definition_t

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
