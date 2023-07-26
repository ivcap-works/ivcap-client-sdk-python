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
        {'command': ['Rerum voluptas sit perferendis tempora deserunt.', 'Excepturi impedit cupiditate et nihil.', 'Aut
            ipsum qui necessitatibus quidem sint.'], 'cpu': {'limit': 'Quaerat nulla iure illum eum.', 'request': 'Est iusto
            eum rerum dolores sed.'}, 'image': 'Nulla corporis unde aperiam.', 'memory': {'limit': 'Quaerat nulla iure illum
            eum.', 'request': 'Est iusto eum rerum dolores sed.'}}

    Attributes:
        command (Union[Unset, List[str]]): Command to start the container - needed for some container runtimes Example:
            ['Iusto asperiores ratione dolore dolor ut nisi.', 'Dolorem dignissimos atque reiciendis perferendis qui
            omnis.', 'Officiis vel eius in asperiores voluptatem ut.', 'Corporis voluptatibus.'].
        cpu (Union[Unset, ResourceMemoryT]): See
            and https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/ for units Example:
            {'limit': 'Ipsam cumque voluptatem.', 'request': 'Eaque cumque ipsa eum laborum corporis.'}.
        image (Union[Unset, str]): container image name Example: Sed voluptas sapiente nihil..
        memory (Union[Unset, ResourceMemoryT]): See
            and https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/ for units Example:
            {'limit': 'Ipsam cumque voluptatem.', 'request': 'Eaque cumque ipsa eum laborum corporis.'}.
    """

    command: Union[Unset, List[str]] = UNSET
    cpu: Union[Unset, "ResourceMemoryT"] = UNSET
    image: Union[Unset, str] = UNSET
    memory: Union[Unset, "ResourceMemoryT"] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command: Union[Unset, List[str]] = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        cpu: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cpu, Unset):
            cpu = self.cpu.to_dict()

        image = self.image
        memory: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.memory, Unset):
            memory = self.memory.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command is not UNSET:
            field_dict["command"] = command
        if cpu is not UNSET:
            field_dict["cpu"] = cpu
        if image is not UNSET:
            field_dict["image"] = image
        if memory is not UNSET:
            field_dict["memory"] = memory

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.resource_memory_t import ResourceMemoryT

        d = src_dict.copy()
        command = cast(List[str], d.pop("command", UNSET))

        _cpu = d.pop("cpu", UNSET)
        cpu: Union[Unset, ResourceMemoryT]
        if isinstance(_cpu, Unset):
            cpu = UNSET
        else:
            cpu = ResourceMemoryT.from_dict(_cpu)

        image = d.pop("image", UNSET)

        _memory = d.pop("memory", UNSET)
        memory: Union[Unset, ResourceMemoryT]
        if isinstance(_memory, Unset):
            memory = UNSET
        else:
            memory = ResourceMemoryT.from_dict(_memory)

        basic_workflow_opts_t = cls(
            command=command,
            cpu=cpu,
            image=image,
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
