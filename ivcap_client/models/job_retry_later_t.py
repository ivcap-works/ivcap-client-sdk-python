from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="JobRetryLaterT")


@_attrs_define
class JobRetryLaterT:
    """Requested job hasn't finished yet, call back later

    Example:
        {'job-id': 'Ut vel.', 'location': 'Rerum voluptates molestiae perferendis quis a aut.', 'retry-later':
            2954767685796848223}

    Attributes:
        location (str): the URL for the job Example: Ab aspernatur architecto ullam dolore et..
        retry_later (int): The time in seconds after which an update may be available Example: 6518556580877944646.
        job_id (Union[Unset, str]): the ID of the job Example: Non sapiente labore iste..
    """

    location: str
    retry_later: int
    job_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        location = self.location

        retry_later = self.retry_later

        job_id = self.job_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "location": location,
                "retry-later": retry_later,
            }
        )
        if job_id is not UNSET:
            field_dict["job-id"] = job_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        location = d.pop("location")

        retry_later = d.pop("retry-later")

        job_id = d.pop("job-id", UNSET)

        job_retry_later_t = cls(
            location=location,
            retry_later=retry_later,
            job_id=job_id,
        )

        job_retry_later_t.additional_properties = d
        return job_retry_later_t

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
