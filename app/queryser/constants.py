import enum
QUERY_MODEL = "query_model"


class Table(enum.StrEnum):
    EMPLOYEE = "EMPLOYEE"
    TRADE_UNION = "TRADE_UNION"

    @classmethod
    def keys(cls, exclude: str | None = None) -> list["Table"]:
        return [table for table in cls if table != exclude]


class States(enum.Enum):
    ...


class IndexType(enum.StrEnum):
    PRIMARY = "primary"
    NONCLUSTERED = "nonclustered"


class ColumnType(enum.StrEnum):
    NUMBER = "number"
    TEXT = "text"
    DATE = "date"
    BOOLEAN = "boolean"
    UUID = "uuid"
    ENUM = "enum"
