import enum
from typing import Any, Union
from queryser.constants import Table
import pydantic


class FilterClause(pydantic.BaseModel):
    column: str


class EqualityFilter(FilterClause):
    negated: bool = pydantic.Field(False)
    value: Any


class RangeFilter(FilterClause):
    min_value: Any = None
    max_value: Any = None


class QueryType(enum.StrEnum):
    NORMAL = enum.auto()
    JOIN = enum.auto()


class SimpleQueryInfo(pydantic.BaseModel):
    table: Table | None = None
    res_attrs: list[str] = pydantic.Field(default_factory=list)
    where_attrs: list[Union[EqualityFilter, RangeFilter]] = pydantic.Field(
        default_factory=list
    )


class JoinQueryInfo(pydantic.BaseModel):
    table_1_query: SimpleQueryInfo
    table_2_query: SimpleQueryInfo
    table_1_attr: str
    table_2_attr: str


class QueryInfo(pydantic.BaseModel):
    type: QueryType = QueryType.NORMAL
    simple: SimpleQueryInfo | None = None
    join: JoinQueryInfo | None = None
