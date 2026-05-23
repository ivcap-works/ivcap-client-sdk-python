from enum import Enum


class ServiceStatusRTStatus(str, Enum):
    ACTIVE = "active"
    ERROR = "error"
    INACTIVE = "inactive"

    def __str__(self) -> str:
        return str(self.value)
