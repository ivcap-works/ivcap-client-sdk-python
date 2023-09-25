from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define, field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_memory_t import ResourceMemoryT


T = TypeVar("T", bound="BasicWorkflowOptsT")


@define
class BasicWorkflowOptsT:
    """
    Example:
        {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'image': 'alpine',
            'memory': {'limit': '100Mi', 'request': '10Mi'}}

    Attributes:
        command (List[str]): Command to start the container - needed for some container runtimes Example: ['/bin/sh',
            '-c', 'echo $PATH'].
        image (str): container image name Example: alpine.
        cpu (Union[Unset, ResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Eos soluta modi aut et.', 'request': 'Qui
            suscipit ullam et.'}.
        memory (Union[Unset, ResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Eos soluta modi aut et.', 'request': 'Qui
            suscipit ullam et.'}.
    """

    command: List[str]
    image: str
    cpu: Union[Unset, "ResourceMemoryT"] = UNSET
    memory: Union[Unset, "ResourceMemoryT"] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command

        image = self.image
        cpu: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        memory: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "command": command,
                "image": image,
            }
        )
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if memory is not UNSET:
            field_dict["memory"] = memory

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resource_memory_t import ResourceMemoryT

        d = src_dict.copy()
        command = cast(List[str], d.pop("command"))

        image = d.pop("image")

        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, ResourceMemoryT]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = ResourceMemoryT.from_dict(_cpu)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, ResourceMemoryT]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = ResourceMemoryT.from_dict(_memory)

        basic_workflow_opts_t = cls(
            command=command,
            image=image,
            cpu=cpu,
            memory=memory,
        )

        basic_workflow_opts_t.additional_properties = d
        return basic_workflow_opts_t

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
