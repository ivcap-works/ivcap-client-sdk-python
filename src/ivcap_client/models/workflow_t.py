from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.basic_workflow_opts_t import BasicWorkflowOptsT


T = TypeVar("T", bound="WorkflowT")


@_attrs_define
class WorkflowT:
    """Defines the workflow to use to execute this service. Currently supported 'types' are 'basic'
    and 'argo'. In case of 'basic', use the 'basic' element for further parameters. In the current implementation
    'opts' is expected to contain the same schema as 'basic'

       Example:
           {'argo': 'Repellat reiciendis.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m',
               'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type':
               'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Et aut autem deserunt sit architecto.', 'memory':
               {'limit': '100Mi', 'request': '10Mi'}, 'shared-memory': '1Gi'}, 'type': 'basic'}

       Attributes:
           type (str): Type of workflow Example: basic.
           argo (Union[Unset, File]): Defines the workflow using argo's WF schema Example: Accusamus commodi..
           basic (Union[Unset, BasicWorkflowOptsT]):  Example: {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu':
               {'limit': '100m', 'request': '10m'}, 'ephemeral-storage': {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2,
               'gpu-type': 'nvidia-tesla-t4', 'image': 'alpine', 'image-pull-policy': 'Sit vel.', 'memory': {'limit': '100Mi',
               'request': '10Mi'}, 'shared-memory': '1Gi'}.
    """

    type: str
    argo: Union[Unset, File] = UNSET
    basic: Union[Unset, "BasicWorkflowOptsT"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type

        argo: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.argo, Unset):
            argo = self.argo.to_tuple()

        basic: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.basic, Unset):
            basic = self.basic.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if argo is not UNSET:
            field_dict["argo"] = argo
        if basic is not UNSET:
            field_dict["basic"] = basic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_workflow_opts_t import BasicWorkflowOptsT

        d = src_dict.copy()
        type = d.pop("type")

        _argo = d.pop("argo", UNSET)
        argo: Union[Unset, File]
        if isinstance(_argo, Unset):
            argo = UNSET
        else:
            argo = File(payload=BytesIO(_argo))

        _basic = d.pop("basic", UNSET)
        basic: Union[Unset, BasicWorkflowOptsT]
        if isinstance(_basic, Unset):
            basic = UNSET
        else:
            basic = BasicWorkflowOptsT.from_dict(_basic)

        workflow_t = cls(
            type=type,
            argo=argo,
            basic=basic,
        )

        workflow_t.additional_properties = d
        return workflow_t

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
