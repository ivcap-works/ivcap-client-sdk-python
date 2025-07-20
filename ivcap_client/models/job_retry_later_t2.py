from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobRetryLaterT2")


@_attrs_define
class JobRetryLaterT2:
    """Requested job hasn't finished yet, call back later

    Example:
        {'job-id': 'Laudantium exercitationem.', 'retry-later': 6557700639310868297}

    Attributes:
        retry_later (int): The time in seconds after which an update may be available Example: 2725599725000718993.
        job_id (Union[Unset, str]): the ID of the job Example: Porro et ut dolores expedita..
    """

    retry_later: int
    job_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        retry_later = self.retry_later

        job_id = self.job_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "retry-later": retry_later,
            }
        )
        if job_id is not UNSET:
            field_dict["job-id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        retry_later = d.pop("retry-later")

        job_id = d.pop("job-id", UNSET)

        job_retry_later_t2 = cls(
            retry_later=retry_later,
            job_id=job_id,
        )

        job_retry_later_t2.additional_properties = d
        return job_retry_later_t2

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
