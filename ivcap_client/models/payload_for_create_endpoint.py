from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PayloadForCreateEndpoint")


@_attrs_define
class PayloadForCreateEndpoint:
    """
    Example:
        {'description': 'Events for the event service', 'name': 'events', 'policy':
            'urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        name (str): Optional Name for the queue. Cannot contain whitespace, ., *, >, path separators (forward or
            backwards slash), and non-printable characters. Example: events.
        description (Union[Unset, str]): More detailed description of the queue. Example: Events for the event service.
        policy (Union[Unset, str]): Reference to policy used Example:
            urn:ivcap:policy:123e4567-e89b-12d3-a456-426614174000.
    """

    name: str
    description: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        policy = self.policy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description", UNSET)

        policy = d.pop("policy", UNSET)

        payload_for_create_endpoint = cls(
            name=name,
            description=description,
            policy=policy,
        )

        payload_for_create_endpoint.additional_properties = d
        return payload_for_create_endpoint

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
