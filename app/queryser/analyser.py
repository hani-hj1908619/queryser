from itertools import permutations
import math

import pandas as pd
from queryser.constants import IndexType, Table

from queryser.query import EqualityFilter, RangeFilter, Cost, QueryInfo, QueryType
import repo

def get_filter_cost(
    df: pd.DataFrame,
    filterr: EqualityFilter | RangeFilter,
) -> Cost:
    if not filterr.table:
        raise ValueError("Filter table is not set")
    
    col_stat = repo.read_column_stats(table=filterr.table, column=filterr.column)
    
    if isinstance(filterr, EqualityFilter):
        
        if col_stat.column_type == 'number':
            filterr.value = float(filterr.value)
        
        if col_stat.index_type == IndexType.PRIMARY:
            if filterr.negated:
                return Cost(
                    algorithm_name="Linear Search",
                    equation="n",
                    value=df.shape[0],
                )
            return Cost(
                algorithm_name="Binary Search",
                equation="log(n)",
                value=math.log(df.shape[0], 2) if df.shape[0] else 0,
            )
        elif col_stat.index_type == IndexType.NONCLUSTERED:
            s = df[df[filterr.column] == filterr.value].shape[0]
            if filterr.negated:
                return Cost(
                    algorithm_name="Linear Search",
                    equation="n",
                    value=df.shape[0] if df.shape[0] else 0,
                )
            elif col_stat.is_unique:
                return Cost(
                    algorithm_name="B+ Tree Search",
                    equation="h + 1",
                    value=math.log(df.shape[0], 2) + 1 if df.shape[0] else 0,
                )
            else:
                return Cost(
                    algorithm_name="B+ Tree Search + Sequential Scan",
                    equation="h + s",
                    value=math.log(df.shape[0], 2) + s if df.shape[0] else 0,
                )   
        else:
            return Cost(
                algorithm_name="Linear Search",
                equation="n",
                value=df.shape[0],
            )
    elif isinstance(filterr, RangeFilter):
        
        if col_stat.column_type == 'number':
            if filterr.min_value is not None:
                filterr.min_value = float(filterr.min_value)
            if filterr.max_value is not None:
                filterr.max_value = float(filterr.max_value)
        
        dd = df.copy()
        if filterr.min_value is not None:
            dd = dd[dd[filterr.column] >= filterr.min_value]
        if filterr.max_value is not None:
            dd = dd[dd[filterr.column] <= filterr.max_value]
        s = dd.shape[0]
        
        if col_stat.index_type == IndexType.PRIMARY:
            return Cost(
                algorithm_name="Range Binary Search",
                equation="log(n) + r",
                value=math.log(df.shape[0], 2) + s if df.shape[0] else 0,
            )
        elif col_stat.index_type == IndexType.NONCLUSTERED:
            return Cost(
                algorithm_name="Range B+ Tree Search",
                equation="h + r",
                value=math.log(df.shape[0], 2) + s if df.shape[0] else 0,
            )
        else:
            return Cost(
                algorithm_name="Linear Search",
                equation="n",
                value=df.shape[0],
            )

def get_join_cost(df1: pd.DataFrame, df2: pd.DataFrame, final_df: pd.DataFrame) -> Cost:
    if df1.shape[0] == 0 or df2.shape[0] == 0:
        value = 0
    else:
        value = (
            df1.shape[0] *math.log(df1.shape[0], 2)
            + df1.shape[0]
            + df2.shape[0] 
            + final_df.shape[0]
        )
    return Cost(
        algorithm_name="Sort Merge Join",
        equation="Br*log2(Br) + Br + Bs + (js * Br * Bs)/Bfr",
        value=value,
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
    df: pd.DataFrame,
    table: Table,
    filterrs: list[tuple[EqualityFilter | RangeFilter]],
) -> tuple[list[list[EqualityFilter | RangeFilter]], pd.DataFrame]:
    clauses_perms: list[list[EqualityFilter | RangeFilter]] = list(
        permutations(filterrs, len(filterrs))
    )
    perms: list[list[EqualityFilter | RangeFilter]] = []

    for perm in clauses_perms:
        curr_df = df.copy()
        clauses: list[EqualityFilter | RangeFilter] = []
        for clause in perm:
            clause.table = table
            initial_size = curr_df.shape[0]
            cost = get_filter_cost(curr_df, clause)
            col_type = repo.read_column_stats(table=table, column=clause.column).column_type
            if isinstance(clause, EqualityFilter):
                if col_type == 'number':
                    clause.value = float(clause.value)
                if clause.negated:
                    curr_df: pd.DataFrame = curr_df[curr_df[clause.column] != clause.value]
                else:
                    curr_df: pd.DataFrame = curr_df[curr_df[clause.column] == clause.value]
            elif isinstance(clause, RangeFilter):
                if col_type == 'number':
                    if clause.min_value is not None:
                        clause.min_value = float(clause.min_value)
                    if clause.max_value is not None:
                        clause.max_value = float(clause.max_value)
                if clause.min_value is not None:
                    curr_df = curr_df[curr_df[clause.column] >= clause.min_value]
                if clause.max_value is not None:
                    curr_df = curr_df[curr_df[clause.column] <= clause.max_value]
            else:
                raise ValueError(f"Invalid clause type {type(clause)}")

            cost.matched_size = curr_df.shape[0]
            cost.initial_size = initial_size
            new_clause = clause.model_copy()
            new_clause.cost = cost
            clauses.append(new_clause)

        perms.append(clauses)

    return perms, curr_df


def get_join_select_costs_post(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_filterrs: list[tuple[EqualityFilter | RangeFilter]],
    df2_filterrs: list[tuple[EqualityFilter | RangeFilter]],
) -> tuple[
    list[list[EqualityFilter | RangeFilter]],
    list[list[EqualityFilter | RangeFilter]],
    Cost,
    pd.DataFrame,
]: 
    df1_before, df2_before = df1.copy(), df2.copy()
    df1_select_cost, df1_after = get_simple_select_costs(df1_before, Table.EMPLOYEE, df1_filterrs)
    df2_select_cost, df2_after = get_simple_select_costs(df2_before, Table.TRADE_UNION, df2_filterrs)
    
    final_df = pd.merge(df1_after, df2_after, left_on="trade_union_id", right_on="id")
    
    join_cost = get_join_cost(df1=df1_after, df2=df2_after, final_df=final_df)
        
    return (
        df1_select_cost,
        df2_select_cost,
        join_cost,
        final_df,
    )


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
        query = query_info.join
        
        table_queries = [query.table_1_query, query.table_2_query]
        for table_query in table_queries:
            for condition in table_query.where_attrs:
                table_name = table_query.table
                conditions.append(
                    f"{table_name}.{condition.column} {generate_condition_clause(condition)}"
                )
                col_stat = repo.read_column_stats(
                    table=table_name, column=condition.column
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
                        
    return pd.DataFrame({"Condition": conditions, "Algorithm": algorithms})
