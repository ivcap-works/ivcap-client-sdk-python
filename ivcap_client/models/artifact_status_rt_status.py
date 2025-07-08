from enum import Enum


class ArtifactStatusRTStatus(str, Enum):
    ERROR = "error"
    PARTIAL = "partial"
    PENDING = "pending"
    READY = "ready"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
