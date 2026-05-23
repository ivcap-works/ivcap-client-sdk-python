from enum import Enum


class OrderStatusRTStatus(str, Enum):
    ERROR = "error"
    EXECUTING = "executing"
    FAILED = "failed"
    PENDING = "pending"
    SCHEDULED = "scheduled"
    SUCCEEDED = "succeeded"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
