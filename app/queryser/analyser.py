from itertools import permutations
import math

import pandas as pd
from queryser.constants import IndexType, Table

from queryser.query import EqualityFilter, RangeFilter, Cost, QueryInfo, QueryType
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


def non_key_non_indexed_cost(size: int) -> Cost:
    return Cost(
        algorithm_name="Linear Search",
        equation="b/2 (avg)",
        value=size / 2 if size else 0,
    )


def generate_condition_clause(clause: EqualityFilter | RangeFilter) -> str:
    if isinstance(clause, EqualityFilter):
        if clause.negated:
            return f"!= {clause.value}"
        else:
            return f"= {clause.value}"
    elif isinstance(clause, RangeFilter):
        if clause.min_value and clause.max_value:
            return f"∈ [{clause.min_value}, {clause.max_value}]"
        elif clause.min_value:
            return f"> {clause.min_value}"
        else:
            return f"< {clause.max_value}"
    else:
        raise ValueError(f"Invalid clause type {type(clause)}")


def get_simple_select_costs(
    df: pd.DataFrame, table: Table, filterrs: list[tuple[EqualityFilter | RangeFilter]]
) -> tuple[list[list[EqualityFilter | RangeFilter]], pd.DataFrame]:
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

                if col_stat.index_type == IndexType.PRIMARY:
                    cost = primary_key_cost(initial_size)
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    cost = secondary_key_cost(initial_size)
                else:
                    cost = non_key_non_indexed_cost(initial_size)
                if clause.negated:
                    curr_df: pd.DataFrame = curr_df[curr_df[clause.column] != clause.value]
                    cost.matched_size = initial_size - curr_df.shape[0]
                else:
                    curr_df: pd.DataFrame = curr_df[curr_df[clause.column] == clause.value]
                    cost.matched_size = curr_df.shape[0]
                
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
                    cost = non_key_non_indexed_cost(initial_size)

                cost.matched_size = after_size
                
            else:
                raise ValueError(f"Invalid clause type {type(clause)}")

            cost.initial_size = initial_size
            new_clause = clause.model_copy()
            new_clause.cost = cost
            clauses.append(new_clause)

        perms.append(clauses)

    return perms, curr_df


def get_join_select_costs(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_filterrs: list[tuple[EqualityFilter | RangeFilter]],
    df2_filterrs: list[tuple[EqualityFilter | RangeFilter]],
) -> tuple[
    list[list[EqualityFilter | RangeFilter]],
    list[list[EqualityFilter | RangeFilter]],
    pd.DataFrame,
]:
    t1_perms, df1_latest = get_simple_select_costs(df1, Table.EMPLOYEE, df1_filterrs)
    t2_perms, df2_latest = get_simple_select_costs(df2, Table.TRADE_UNION, df2_filterrs)

    final_df = pd.merge(df1_latest, df2_latest, left_on="trade_union_id", right_on="id")

    perms = []


def get_best_algorithms(query_info: QueryInfo) -> pd.DataFrame:
    conditions = []
    algorithms = []

    if query_info.type == QueryType.NORMAL:
        query = query_info.simple

        for condition in query.where_attrs:
            conditions.append(
                f"{query.table}.{condition.column} {generate_condition_clause(condition)}"
            )

            col_stat = repo.read_column_stats(
                table=query.table, column=condition.column
            )

            if isinstance(condition, EqualityFilter):
                if col_stat.index_type == IndexType.PRIMARY:
                    algorithms.append("Binary Search")
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    algorithms.append("B+ Tree Search")
                else:
                    algorithms.append("Linear Search")
            elif isinstance(condition, RangeFilter):
                if col_stat.index_type == IndexType.PRIMARY:
                    algorithms.append("Binary Search + Sequential Scan")
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    algorithms.append("Range B+ Tree Search")
                else:
                    algorithms.append("Linear Search")

    elif query_info.type == QueryType.JOIN:
        pass

    return pd.DataFrame({"Condition": conditions, "Algorithm": algorithms})
