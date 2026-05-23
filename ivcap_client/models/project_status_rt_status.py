from enum import Enum


class ProjectStatusRTStatus(str, Enum):
    ACTIVE = "active"
    DELETED = "deleted"
    DISABLED = "disabled"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
