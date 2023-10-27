from dataclasses import dataclass, Field
from typing import Any
from queryser.constants import Table

@dataclass
class FilterClause:
    column: str

@dataclass
class EqualityFilter(FilterClause):
    negated: bool = False
    value: Any

@dataclass
class RangeFilter(FilterClause):
    min_value: Any = None
    max_value: Any = None

@dataclass
class SimpleQueryInfo:
    table: Table
    res_attrs: list[str] = Field(default_factory=list)
    where_attrs: list[FilterClause] = Field(default_factory=list)
    