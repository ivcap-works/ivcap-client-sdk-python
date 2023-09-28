from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.basic_workflow_opts_t import BasicWorkflowOptsT


T = TypeVar("T", bound="WorkflowT")


@define
class WorkflowT:
    """Defines the workflow to use to execute this service. Currently supported 'types' are 'basic'
    and 'argo'. In case of 'basic', use the 'basic' element for further parameters. In the current implementation
    'opts' is expected to contain the same schema as 'basic'

    Example:
        {'argo': 'Ullam illum assumenda explicabo aut.', 'basic': {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu':
            {'limit': '100m', 'request': '10m'}, 'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}},
            'opts': 'Et porro ducimus corporis quas.', 'type': 'basic'}

    Attributes:
        argo (Union[Unset, File]): Defines the workflow using argo's WF schema Example: Dolores quis quaerat consequatur
            quas..
        basic (Union[Unset, BasicWorkflowOptsT]):  Example: {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu':
            {'limit': '100m', 'request': '10m'}, 'image': 'alpine', 'memory': {'limit': '100Mi', 'request': '10Mi'}}.
        opts (Union[Unset, File]): Type specific options - left for backward compatibility, if possible use type
            specific elements Example: Illo dolores inventore odit unde architecto quis..
        type (Union[Unset, str]): Type of workflow Example: basic.
    """

    argo: Union[Unset, File] = UNSET
    basic: Union[Unset, "BasicWorkflowOptsT"] = UNSET
    opts: Union[Unset, File] = UNSET
    type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        argo: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.argo, Unset):
            argo = self.argo.to_tuple()

        basic: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.basic, Unset):
            basic = self.basic.to_dict()

        opts: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.opts, Unset):
            opts = self.opts.to_tuple()

        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if argo is not UNSET:
            field_dict["argo"] = argo
        if basic is not UNSET:
            field_dict["basic"] = basic
        if opts is not UNSET:
            field_dict["opts"] = opts
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.basic_workflow_opts_t import BasicWorkflowOptsT

        d = src_dict.copy()
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

        _opts = d.pop("opts", UNSET)
        opts: Union[Unset, File]
        if isinstance(_opts, Unset):
            opts = UNSET
        else:
            opts = File(payload=BytesIO(_opts))

        type = d.pop("type", UNSET)

        workflow_t = cls(
            argo=argo,
            basic=basic,
            opts=opts,
            type=type,
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
