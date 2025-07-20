from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.x_resource_memory_t import XResourceMemoryT


T = TypeVar("T", bound="XBasicWorkflowOptsT")


@_attrs_define
class XBasicWorkflowOptsT:
    """
    Example:
        {'command': ['/bin/sh', '-c', 'echo $PATH'], 'cpu': {'limit': '100m', 'request': '10m'}, 'ephemeral-storage':
            {'limit': '4Gi', 'request': '2Gi'}, 'gpu-number': 2, 'gpu-type': 'nvidia-tesla-t4', 'image': 'alpine', 'image-
            pull-policy': 'Repellendus eos labore quasi assumenda aut.', 'memory': {'limit': '100Mi', 'request': '10Mi'},
            'shared-memory': '1Gi'}

    Attributes:
        command (list[str]): Command to start the container - needed for some container runtimes Example: ['/bin/sh',
            '-c', 'echo $PATH'].
        image (str): container image name Example: alpine.
        cpu (Union[Unset, XResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Iste nemo et harum hic qui voluptas.',
            'request': 'Minima ut ipsam.'}.
        ephemeral_storage (Union[Unset, XResourceMemoryT]): See
            https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-units-in-kubernetes for
            units Example: {'limit': 'Iste nemo et harum hic qui voluptas.', 'request': 'Minima ut ipsam.'}.
        gpu_number (Union[Unset, int]): Defines number of required gpu Example: 2.
        gpu_type (Union[Unset, str]): Defines required gpu type Example: nvidia-tesla-t4.
        image_pull_policy (Union[Unset, str]): Optionally definesq the image pull policy Default: 'IfNotPresent'.
            Example: Sit pariatur..
        memory (Union[Unset, XResourceMemoryT]): See https://kubernetes.io/docs/concepts/configuration/manage-resources-
            containers/#resource-units-in-kubernetes for units Example: {'limit': 'Iste nemo et harum hic qui voluptas.',
            'request': 'Minima ut ipsam.'}.
        shared_memory (Union[Unset, str]): Defines needed amount of shared-memory Example: 1Gi.
    """

    command: list[str]
    image: str
    cpu: Union[Unset, "XResourceMemoryT"] = UNSET
    ephemeral_storage: Union[Unset, "XResourceMemoryT"] = UNSET
    gpu_number: Union[Unset, int] = UNSET
    gpu_type: Union[Unset, str] = UNSET
    image_pull_policy: Union[Unset, str] = "IfNotPresent"
    memory: Union[Unset, "XResourceMemoryT"] = UNSET
    shared_memory: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        command = self.command

        image = self.image

        cpu: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        ephemeral_storage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ephemeral_storage, Unset):
            ephemeral_storage = self.ephemeral_storage.to_dict()

        gpu_number = self.gpu_number

        gpu_type = self.gpu_type

        image_pull_policy = self.image_pull_policy

        memory: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        shared_memory = self.shared_memory

        field_dict: dict[str, Any] = {}
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.x_resource_memory_t import XResourceMemoryT

        d = src_dict.copy()
        command = cast(list[str], d.pop("command"))

        image = d.pop("image")

        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, XResourceMemoryT]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = XResourceMemoryT.from_dict(_cpu)

        _ephemeral_storage = d.pop("ephemeral-storage", UNSET)
        ephemeral_storage: Union[Unset, XResourceMemoryT]
        if isinstance(_ephemeral_storage, Unset):
            ephemeral_storage = UNSET
        else:
            ephemeral_storage = XResourceMemoryT.from_dict(_ephemeral_storage)

        gpu_number = d.pop("gpu-number", UNSET)

        gpu_type = d.pop("gpu-type", UNSET)

        image_pull_policy = d.pop("image-pull-policy", UNSET)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, XResourceMemoryT]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = XResourceMemoryT.from_dict(_memory)

        shared_memory = d.pop("shared-memory", UNSET)

        x_basic_workflow_opts_t = cls(
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

        x_basic_workflow_opts_t.additional_properties = d
        return x_basic_workflow_opts_t

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
