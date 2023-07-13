from enum import Enum


class ArtifactStatusRTStatus(str, Enum):
    PENDING  = "pending"
    PARTIAL  = "partial"
    READY    = "ready"
    ERROR    = "error"
    UNKNOWN  = "unknown"

    def __str__(self) -> str:
        return str(self.value)
