from enum import Enum


class OrderListItemStatus(str, Enum):
    ERROR = "error"
    EXECUTING = "executing"
    FINISHED = "finished"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
