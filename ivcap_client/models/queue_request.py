from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QueueRequest")


@_attrs_define
class QueueRequest:
    """
    Example:
        {'description': 'Events for the event service', 'name': 'events', 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        description (Union[Unset, str]): More detailed description of the queue. Example: Events for the event service.
        name (Union[Unset, str]): Optional Name for the queue. Cannot contain whitespace, ., *, >, path separators
            (forward or backwards slash), and non-printable characters. Example: events.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
    """

    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        name = self.name

        policy = self.policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        policy = d.pop("policy", UNSET)

        queue_request = cls(
            description=description,
            name=name,
            policy=policy,
        )

        queue_request.additional_properties = d
        return queue_request

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
