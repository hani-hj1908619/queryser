import enum
from typing import Self

class Table(enum.StrEnum):
    EMPLOYEE = "EMPLOYEE"
    TRADE_UNION = "TRADE UNION"

    @classmethod
    def keys(cls) -> list[Self]:
        return [table for table in cls]

class States(enum.Enum):
    ...