import streamlit as st
import repo
from queryser.constants import Table

employee_columns = repo.read_employee_table_columns()
employee_key_columns = repo.read_employee_key_columns()
trade_union_columns = repo.read_trade_union_table_columns()
trade_union_key_columns = repo.read_trade_union_key_columns()


def main() -> None:
    st.set_page_config(page_title="Query", layout="wide")
    st.subheader("Select")
    is_join_query = st.checkbox("Is equi-join query", value=False)
    if is_join_query:
        join_query_view()
    else:
        normal_query_view()


def normal_query_view() -> None:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        table = st.selectbox("Table", Table.keys(), index=0)
    with t1_col2:
        t1_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table),
            placeholder="Select columns to be displayed",
        )

    st.subheader("Conditions")
    selection_condition_view()


def join_query_view() -> None:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        table1 = st.selectbox("Table 1", Table.keys(), index=0)
    with t1_col2:
        t1_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table1),
            placeholder="Select columns to be displayed",
        )

    t2_col1, t2_col2 = st.columns(2)
    with t2_col1:
        table2 = st.selectbox("Table 2", Table.keys(), index=1)
    with t2_col2:
        t2_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table2),
            placeholder="Select columns to be displayed",
        )

    st.subheader("Conditions")

    st.caption("Join condition")

    join_cond_col1, join_cond_col2 = st.columns(2)
    with join_cond_col1:
        t1_join_column = st.selectbox(
            f"{table1} join column",
            ["trade_union_id"] if table1 == Table.EMPLOYEE else ["id"],
        )
    with join_cond_col2:
        t2_join_column = st.selectbox(
            f"{table2} join column",
            ["trade_union_id"] if table2 == Table.EMPLOYEE else ["id"],
        )

    selection_condition_view()


def selection_condition_view() -> None:
    st.caption("Selection conditions")

    if "num_conditions" not in st.session_state:
        st.session_state["num_conditions"] = 1

    condition_col1, condition_col2, condition_col3, condition_col4 = st.columns(4)

    for i in range(st.session_state["num_conditions"]):
        with condition_col1:
            condition_type = st.selectbox(
                "Condition type",
                ["Equality", "Range"],
                key=f"condition_type_{i}",
            )

        with condition_col2:
            table = st.selectbox("Table", Table.keys(), key=f"condition_table_{i}")

        with condition_col3:
            condition_column = st.selectbox(
                "Column",
                repo.read_table_key_columns(table),
                key=f"condition_column_{i}",
            )

        with condition_col4:
            if condition_type == "Equality":
                st.text_input("Value", key=f"condition_value_{i}")
            elif condition_type == "Range":
                range_col1, range_col2 = st.columns(2)
                with range_col1:
                    st.text_input("Min", key=f"condition_min_{i}")
                with range_col2:
                    st.text_input("Max", key=f"condition_max_{i}")

    def add_condition() -> None:
        st.session_state["num_conditions"] += 1

    st.button(
        "Add selection condition",
        on_click=lambda: add_condition(),
        key=f"add_condition_button",
    )


main()
