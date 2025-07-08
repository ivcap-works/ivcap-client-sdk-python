from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_memory_t import ResourceMemoryT


T = TypeVar("T", bound="BasicWorkflowOptsT")


@_attrs_define
class BasicWorkflowOptsT:
    """
    Example:
        {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-storage':
            {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-tesla-t4', 'image': 'alpine', 'image-
            pull-policy': 'Accusamus doloremque et dolor ullam dolorem hic.', 'memory': {'limit': '100Mi', 'request':
            '10Mi'}, 'shared-memory': '1Gi'}

    Attributes:
        command (List[str]): Command to start the container - needed for some container runtimes Example: ['/bin/sh',
            '-c', 'echo $PATH'].
        image (str): container image name Example: alpine.
        cpu (Union[Unset, ResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Pariatur sint corrupti.', 'request':
            'Porro blanditiis nihil eligendi perferendis cumque.'}.
        ephemeral_storage (Union[Unset, ResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-
            resources-containers/#resource-units-in-kubernetes for units Example: {'limit': 'Pariatur sint corrupti.',
            'request': 'Porro blanditiis nihil eligendi perferendis cumque.'}.
        gpu_number (Union[Unset, int]): Defines number of required gpu Example: 2.
        gpu_type (Union[Unset, str]): Defines required gpu type Example: nvidia-tesla-t4.
        image_pull_policy (Union[Unset, str]): Optionally definesq the image pull policy Default: 'IfNotPresent'.
            Example: Corporis unde aperiam et nihil..
        memory (Union[Unset, ResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Pariatur sint corrupti.', 'request':
            'Porro blanditiis nihil eligendi perferendis cumque.'}.
        shared_memory (Union[Unset, str]): Defines needed amount of shared-memory Example: 1Gi.
    """

    command: List[str]
    image: str
    cpu: Union[Unset, "ResourceMemoryT"] = UNSET
    ephemeral_storage: Union[Unset, "ResourceMemoryT"] = UNSET
    gpu_number: Union[Unset, int] = UNSET
    gpu_type: Union[Unset, str] = UNSET
    image_pull_policy: Union[Unset, str] = "IfNotPresent"
    memory: Union[Unset, "ResourceMemoryT"] = UNSET
    shared_memory: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command = self.command

        image = self.image

        cpu: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        ephemeral_storage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ephemeral_storage, Unset):
            ephemeral_storage = self.ephemeral_storage.to_dict()

        gpu_number = self.gpu_number

        gpu_type = self.gpu_type

        image_pull_policy = self.image_pull_policy

        memory: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        shared_memory = self.shared_memory

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
        if ephemeral_storage is not UNSET:
            field_dict["ephemeral-storage"] = ephemeral_storage
        if gpu_number is not UNSET:
            field_dict["gpu-number"] = gpu_number
        if gpu_type is not UNSET:
            field_dict["gpu-type"] = gpu_type
        if image_pull_policy is not UNSET:
            field_dict["image-pull-policy"] = image_pull_policy
        if memory is not UNSET:
            field_dict["memory"] = memory
        if shared_memory is not UNSET:
            field_dict["shared-memory"] = shared_memory

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

        _ephemeral_storage = d.pop("ephemeral-storage", UNSET)
        ephemeral_storage: Union[Unset, ResourceMemoryT]
        if isinstance(_ephemeral_storage, Unset):
            ephemeral_storage = UNSET
        else:
            ephemeral_storage = ResourceMemoryT.from_dict(_ephemeral_storage)

        gpu_number = d.pop("gpu-number", UNSET)

        gpu_type = d.pop("gpu-type", UNSET)

        image_pull_policy = d.pop("image-pull-policy", UNSET)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, ResourceMemoryT]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = ResourceMemoryT.from_dict(_memory)

        shared_memory = d.pop("shared-memory", UNSET)

        basic_workflow_opts_t = cls(
            command=command,
            image=image,
            cpu=cpu,
            ephemeral_storage=ephemeral_storage,
            gpu_number=gpu_number,
            gpu_type=gpu_type,
            image_pull_policy=image_pull_policy,
            memory=memory,
            shared_memory=shared_memory,
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
