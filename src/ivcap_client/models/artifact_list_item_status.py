from enum import Enum


class ArtifactListItemStatus(str, Enum):
    PENDING  = "pending"
    PARTIAL  = "partial"
    READY    = "ready"
    ERROR    = "error"
    UNKNOWN  = "unknown"

    def __str__(self) -> str:
        return str(self.value)
