from time import sleep
import streamlit as st
from streamlit_extras.switch_page_button import switch_page 
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
    
    if QUERY_MODEL in st.session_state:
        query_info: QueryInfo = st.session_state[QUERY_MODEL]
        if query_info.type == QueryType.NORMAL:
            simple_select_cost(query_info.simple)
        elif query_info.type == QueryType.JOIN:
            join_select_cost(query_info.join)
    else:
        st.error("Please select a query first", icon='❗')
        with st.spinner("Redirecting to Query page..."):
            sleep(1.5)
            switch_page("Query")
        
        
def simple_select_cost(query_info: SimpleQueryInfo) -> None:
    df = repo.read_employee_table() if query_info.table == Table.EMPLOYEE else repo.read_trade_union_table()
    clauses_perms = list(permutations(query_info.where_attrs, len(query_info.where_attrs)))
    costs = []
    for perm in clauses_perms:
        curr_df, curr_cost = df.copy(), []
        for clause in perm:
            size = curr_df.size
            col_stat = repo.read_column_stats(table=query_info.table, column=clause.column)
            if isinstance(clause, EqualityFilter):
                
                if col_stat.index_type == IndexType.PRIMARY:
                    cost = primary_key_cost(size)
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    cost = secondary_key_cost(size)
                else:
                    raise ValueError(f"Invalid index type {col_stat.index_type}")
                
                if clause.negated:
                    curr_df = curr_df[curr_df[clause.column] != clause.value]
                else:
                    curr_df = curr_df[curr_df[clause.column] == clause.value]
                
                curr_cost.append(cost)

            elif isinstance(clause, RangeFilter):

                if clause.min_value is not None and clause.max_value is not None:
                    curr_df = curr_df[curr_df[clause.column] >= clause.min_value]
                    curr_df = curr_df[curr_df[clause.column] <= clause.max_value]
                elif clause.min_value is not None:
                    curr_df = curr_df[curr_df[clause.column] >= clause.min_value]
                elif clause.max_value is not None:
                    curr_df = curr_df[curr_df[clause.column] <= clause.max_value]

                if col_stat.index_type == IndexType.PRIMARY:
                    cost = primary_key_range_cost(size=size, range_size=curr_df.size)
                elif col_stat.index_type == IndexType.NONCLUSTERED:
                    cost = secondary_key_range_cost(size=size, range_size=curr_df.size)
                else:
                    raise ValueError(f"Invalid index type {col_stat.index_type}")

                curr_cost.append(cost)
        
        st.write(curr_cost)

def join_select_cost(query_info: JoinQueryInfo) -> None:
    pass

main()