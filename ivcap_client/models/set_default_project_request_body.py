from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetDefaultProjectRequestBody")


@_attrs_define
class SetDefaultProjectRequestBody:
    """
    Example:
        {'project_urn': 'urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f', 'user_urn':
            'urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468'}

    Attributes:
        project_urn (str): Project URN Example: urn:ivcap:project:59c76bc8-721b-409d-8a32-6d560680e89f.
        user_urn (Union[Unset, str]): User URN Example: urn:ivcap:user:0b755f67-4d03-4d82-b208-4d6a0ae16468.
    """

    project_urn: str
    user_urn: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_urn = self.project_urn

        user_urn = self.user_urn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_urn": project_urn,
            }
        )
        if user_urn is not UNSET:
            field_dict["user_urn"] = user_urn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        project_urn = d.pop("project_urn")

        user_urn = d.pop("user_urn", UNSET)

        set_default_project_request_body = cls(
            project_urn=project_urn,
            user_urn=user_urn,
        )

        set_default_project_request_body.additional_properties = d
        return set_default_project_request_body

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
