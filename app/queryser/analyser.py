from dataclasses import dataclass
from itertools import permutations
import math

import pandas as pd
from queryser.constants import IndexType, Table

from queryser.query import EqualityFilter, RangeFilter, Cost
import repo


def primary_key_cost(size: int) -> Cost:
    return Cost(
        algorithm_name="Binary Search",
        equation="log(n)",
        value=math.log(size, 2) if size else 0,
    )


def secondary_key_cost(size: int) -> Cost:
    return Cost(
        algorithm_name="B+ Tree Search",
        equation="h + 1",
        value=math.log(size, 2) + 1 if size else 0,
    )


def primary_key_range_cost(size: int, range_size: int) -> Cost:
    return Cost(
        algorithm_name="Range Binary Search",
        equation="log(n) + r",
        value=math.log(size, 2) + range_size if size else 0,
    )


def secondary_key_range_cost(size: int, range_size: int) -> Cost:
    return Cost(
        algorithm_name="Range B+ Tree Search",
        equation="h + r",
        value=math.log(size, 2) + range_size if size else 0,
    )


def get_simple_select_costs(
    df: pd.DataFrame, table: Table, filterrs: list[tuple[EqualityFilter | RangeFilter]]
) -> list[list[EqualityFilter | RangeFilter]]:
    clauses_perms: list[list[EqualityFilter | RangeFilter]] = list(
        permutations(filterrs, len(filterrs))
    )
    perms: list[list[EqualityFilter | RangeFilter]] = []

    for perm in clauses_perms:
        curr_df = df.copy()
        clauses: list[EqualityFilter | RangeFilter] = []
        for clause in perm:
            col_stat = repo.read_column_stats(table=table, column=clause.column)
            initial_size = curr_df.shape[0]

            if isinstance(clause, EqualityFilter):
                if clause.negated:
                    curr_df: pd.DataFrame = curr_df[
                        curr_df[clause.column] != clause.value
                    ]
                else:
                    curr_df: pd.DataFrame = curr_df[
                        curr_df[clause.column] == clause.value
                    ]

                after_size = curr_df.shape[0]

                if col_stat.index_type == IndexType.PRIMARY:
                    cost = primary_key_cost(initial_size)
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    cost = secondary_key_cost(initial_size)
                else:
                    raise ValueError(f"Invalid index type {col_stat.index_type}")

            elif isinstance(clause, RangeFilter):
                if clause.min_value is not None and clause.max_value is not None:
                    curr_df = curr_df[curr_df[clause.column] >= clause.min_value]
                    curr_df = curr_df[curr_df[clause.column] <= clause.max_value]
                elif clause.min_value is not None:
                    curr_df = curr_df[curr_df[clause.column] >= clause.min_value]
                elif clause.max_value is not None:
                    curr_df = curr_df[curr_df[clause.column] <= clause.max_value]

                after_size = curr_df.shape[0]

                if col_stat.index_type == IndexType.PRIMARY:
                    cost = primary_key_range_cost(
                        size=initial_size, range_size=after_size
                    )
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    cost = secondary_key_range_cost(
                        size=initial_size, range_size=after_size
                    )
                else:
                    raise ValueError(f"Invalid index type {col_stat.index_type}")

            else:
                raise ValueError(f"Invalid clause type {type(clause)}")

            cost.initial_size = initial_size
            cost.matched_size = initial_size - after_size
            new_clause = clause.model_copy()
            new_clause.cost = cost
            clauses.append(new_clause)

        perms.append(clauses)

    return perms
