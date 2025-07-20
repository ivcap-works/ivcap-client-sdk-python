from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrderTopResultItem")


@_attrs_define
class OrderTopResultItem:
    """
    Example:
        {'container': 'Assumenda dolore.', 'cpu': 'Assumenda dolorem eveniet illo repellendus atque ad.', 'ephemeral-
            storage': 'Vitae ut quasi minus et ad eius.', 'memory': 'Adipisci atque itaque aut nostrum maiores.', 'storage':
            'Placeat tenetur qui libero et iusto et.'}

    Attributes:
        container (str): container Example: Quo et aut quas..
        cpu (str): cpu Example: Animi minus sapiente incidunt quas..
        ephemeral_storage (str): ephemeral-storage Example: Soluta est iure accusamus tenetur dolorem..
        memory (str): memory Example: Vel a aut temporibus..
        storage (str): storage Example: Dolores quod ipsa..
    """

    container: str
    cpu: str
    ephemeral_storage: str
    memory: str
    storage: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        container = self.container

        cpu = self.cpu

        ephemeral_storage = self.ephemeral_storage

        memory = self.memory

        storage = self.storage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "container": container,
                "cpu": cpu,
                "ephemeral-storage": ephemeral_storage,
                "memory": memory,
                "storage": storage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        container = d.pop("container")

        cpu = d.pop("cpu")

        ephemeral_storage = d.pop("ephemeral-storage")

        memory = d.pop("memory")

        storage = d.pop("storage")

        order_top_result_item = cls(
            container=container,
            cpu=cpu,
            ephemeral_storage=ephemeral_storage,
            memory=memory,
            storage=storage,
        )

        order_top_result_item.additional_properties = d
        return order_top_result_item

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
