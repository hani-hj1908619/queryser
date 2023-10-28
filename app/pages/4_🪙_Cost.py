import math
from time import sleep
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from queryser import analyser 
from queryser.constants import QUERY_MODEL, IndexType
from queryser.query import (
    QueryInfo,
    SimpleQueryInfo,
    JoinQueryInfo,
    QueryType,
    Table,
    EqualityFilter,
    RangeFilter,
)
from queryser.analyser import (
    Cost,
    primary_key_cost,
    primary_key_range_cost,
    secondary_key_cost,
    secondary_key_range_cost,
)
from itertools import permutations
import pandas as pd
import repo

def main() -> None:
    st.set_page_config(page_title="Costs", page_icon='🪙', layout="wide")
    
    st.title("Query Costs\n")
    
    if QUERY_MODEL not in st.session_state:
        st.error("Please select a query first", icon='❗')
        with st.spinner("Redirecting to Query page..."):
            sleep(1.5)
            switch_page("Query")   
        
    query_info: QueryInfo = st.session_state[QUERY_MODEL]
    if query_info.type == QueryType.NORMAL:
        simple_select_cost(query_info.simple)
    elif query_info.type == QueryType.JOIN:
        join_select_cost(query_info.join)


def sum_costs(perm: list[EqualityFilter | RangeFilter]) -> float:
    return sum([cost.cost.value for cost in perm])

def condition_clause(clause: EqualityFilter | RangeFilter) -> str:
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


def simple_select_cost(query_info: SimpleQueryInfo) -> None:
    df = repo.read_employee_table() if query_info.table == Table.EMPLOYEE else repo.read_trade_union_table()
    
    st.subheader("Initial table")
    st.dataframe(df)
    
    perms = analyser.get_simple_select_costs(df, query_info.table, query_info.where_attrs)
    perms.sort(key=lambda perm: sum_costs(perm))

    st.subheader("Query permutations")
    
    for i, perm in enumerate(perms, start=1):
        sum = sum_costs(perm)
        with st.expander(f"Perm({i}) - Cost: {math.ceil(sum)}"):
            st.dataframe(
                pd.DataFrame({
                    "Table Size": [clause.cost.initial_size for clause in perm],
                    "Column": [clause.column for clause in perm],
                    "Condition": [condition_clause(clause) for clause in perm],
                    "Algorithm": [clause.cost.algorithm_name for clause in perm],
                    "Matched": [clause.cost.matched_size for clause in perm],
                    "Equation": [clause.cost.equation for clause in perm],
                    "Cost": [math.ceil(clause.cost.value) for clause in perm],
                }),
                use_container_width=True
            )

def join_select_cost(query_info: JoinQueryInfo) -> None:
    pass

main()