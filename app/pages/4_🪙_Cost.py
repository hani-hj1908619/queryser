import math
from time import sleep
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from queryser import analyser
from queryser.constants import QUERY_MODEL
from queryser.query import (
    QueryInfo,
    SimpleQueryInfo,
    JoinQueryInfo,
    QueryType,
    Table,
    EqualityFilter,
    RangeFilter,
)
import pandas as pd
import repo


def main() -> None:
    st.set_page_config(page_title="Costs", page_icon="🪙", layout="wide")

    st.title("Query Costs\n")

    if QUERY_MODEL not in st.session_state:
        st.error("Please select a query first", icon="❗")
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


def simple_select_cost(query_info: SimpleQueryInfo) -> None:
    df = (
        repo.read_employee_table()
        if query_info.table == Table.EMPLOYEE
        else repo.read_trade_union_table()
    )

    st.subheader("Initial table")
    st.dataframe(df)

    perms, _ = analyser.get_simple_select_costs(
        df, query_info.table, query_info.where_attrs
    )
    perms.sort(key=lambda perm: sum_costs(perm))

    st.subheader("Query permutations")

    for i, perm in enumerate(perms, start=1):
        sum = sum_costs(perm) or df.shape[0]
        with st.expander(f"Perm({i}) - Cost: {math.ceil(sum)}"):
            if sum == df.shape[0]:
                st.write("No filtering")
            else:
                st.dataframe(
                    pd.DataFrame(
                        {
                            "Table Size": [clause.cost.initial_size for clause in perm],
                            "Column": [clause.column for clause in perm],
                            "Condition": [
                                analyser.generate_condition_clause(clause)
                                for clause in perm
                            ],
                            "Algorithm": [
                                clause.cost.algorithm_name for clause in perm
                            ],
                            "Matched": [clause.cost.matched_size for clause in perm],
                            "Equation": [clause.cost.equation for clause in perm],
                            "Cost": [math.ceil(clause.cost.value) for clause in perm],
                        }
                    ),
                    use_container_width=True,
                )


def join_select_cost(query_info: JoinQueryInfo) -> None:
    df1 = repo.read_employee_table()
    df2 = repo.read_trade_union_table()

    st.subheader("Initial tables")
    st.subheader("Employee")
    st.dataframe(df1)
    st.subheader("Trade Union")
    st.dataframe(df2)

    df1_perms, df2_perms, join_cost, final_df = analyser.get_join_select_costs_post(
        df1, 
        df2,
        query_info.table_1_query.where_attrs,
        query_info.table_2_query.where_attrs,
    )
    
    
    df1_perms.sort(key=lambda perm: sum_costs(perm))
    df2_perms.sort(key=lambda perm: sum_costs(perm))
    
    st.subheader("Employee filters permutations")
    for i, perm in enumerate(df1_perms, start=1):
        sum = sum_costs(perm) or df1.shape[0]
        with st.expander(f"Perm({i}) - Cost: {math.ceil(sum)}"):
            if sum == df1.shape[0]:
                st.write("No filtering")
            else:
                st.dataframe(
                    pd.DataFrame(
                        {
                            "Table Size": [clause.cost.initial_size for clause in perm],
                            "Column": [clause.column for clause in perm],
                            "Condition": [
                                analyser.generate_condition_clause(clause)
                                for clause in perm
                            ],
                            "Algorithm": [
                                clause.cost.algorithm_name for clause in perm
                            ],
                            "Matched": [clause.cost.matched_size for clause in perm],
                            "Equation": [clause.cost.equation for clause in perm],
                            "Cost": [math.ceil(clause.cost.value) for clause in perm],
                        }
                    ),
                    use_container_width=True,
                )
    
    st.subheader("Trade Union filters permutations")
    for i, perm in enumerate(df2_perms, start=1):
        sum = sum_costs(perm) or df2.shape[0]
        with st.expander(f"Perm({i}) - Cost: {math.ceil(sum)}"):
            st.dataframe(
                pd.DataFrame(
                    {
                        "Table Size": [clause.cost.initial_size for clause in perm],
                        "Column": [clause.column for clause in perm],
                        "Condition": [
                            analyser.generate_condition_clause(clause)
                            for clause in perm
                        ],
                        "Algorithm": [
                            clause.cost.algorithm_name for clause in perm
                        ],
                        "Matched": [clause.cost.matched_size for clause in perm],
                        "Equation": [clause.cost.equation for clause in perm],
                        "Cost": [math.ceil(clause.cost.value) for clause in perm],
                    }
                ),
                use_container_width=True,
            )
    if not perm:
        st.write("No filtering")
    
    st.subheader("Join cost")
    df1_last_size = df1_perms[-1][-1].cost.matched_size
    df2_last_size = df2_perms[-1][-1].cost.matched_size
    st.dataframe(
        pd.DataFrame(
            {
                "Condition": "Employee.trade_union_id = Trade_union.id",
                "Algorithm": [join_cost.algorithm_name],
                "Equation": [join_cost.equation],
                "Tables Size (Before)": f"{df1_last_size} x {df2_last_size}",
                "Table Size (After)": [final_df.shape[0]],
                "Cost": [math.ceil(join_cost.value)],
            }
        )
    )
    
    st.subheader("Final table")
    st.dataframe(final_df)


main()
