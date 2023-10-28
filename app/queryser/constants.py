import enum
from typing import Self

QUERY_MODEL = "query_model"


class Table(enum.StrEnum):
    EMPLOYEE = "EMPLOYEE"
    TRADE_UNION = "TRADE UNION"

    @classmethod
    def keys(cls, exclude: str | None = None) -> list[Self]:
        return [table for table in cls if table != exclude]


class States(enum.Enum):
    ...


class IndexType(enum.StrEnum):
    PRIMARY = "primary"
    NONCLUSTERED = "nonclustered"
