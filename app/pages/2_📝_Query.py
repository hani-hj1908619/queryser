import streamlit as st
import repo
from queryser.constants import Table
from queryser.query import QueryType, SimpleQueryInfo, QueryInfo
import enum

class State(enum.StrEnum):
    is_join_query = enum.auto()
    num_conditions = enum.auto()
    select_table = enum.auto()

    @classmethod
    def display_columns(cls, i: int | None = None) -> str:
        return f"display_columns_{i}" if i is not None else "display_columns"
    @classmethod
    def join_table(cls, i: int | None = None) -> str:
        return f"join_table_{i}" if i is not None else "join_table"
    @classmethod
    def condition_table(cls, i: int | None = None) -> str:
        return f"condition_table_{i}" if i is not None else "condition_table"
    @classmethod
    def condition_type(cls, i: int | None = None) -> str:
        return f"condition_type_{i}" if i is not None else "condition_type"
    @classmethod
    def condition_column(cls, i: int | None = None) -> str:
        return f"condition_column_{i}" if i is not None else "condition_column"
    @classmethod
    def join_column(cls, i: int | None = None) -> str:
        return f"join_column_{i}" if i is not None else "join_column"
    @classmethod
    def condition_value(cls, i: int | None = None) -> str:
        return f"condition_value_{i}" if i is not None else "condition_value"
    @classmethod
    def condition_min(cls, i: int | None = None) -> str:
        return f"condition_min_{i}" if i is not None else "condition_min"
    @classmethod
    def condition_max(cls, i: int | None = None) -> str:
        return f"condition_max_{i}" if i is not None else "condition_max"

def main() -> None:
    st.set_page_config(page_title="Query", layout="wide")
    st.subheader("Select")
    is_join_query = st.checkbox("Is equi-join query", value=False, key=State.is_join_query)
    if is_join_query:
        join_query_view()
    else:
        normal_query_view()
            
    st.button("Analyse", on_click=analyze)
    
def normal_query_view() -> None:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        table = st.selectbox(
            "Table",
            Table.keys(),
            index=0,
            key=State.select_table
        )
    with t1_col2:
        t1_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table),
            placeholder="Select columns to be displayed",
            key=State.display_columns(),
        )

    st.subheader("Conditions")
    selection_condition_view()


def join_query_view() -> None:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        table1 = st.selectbox(
            "Table 1",
            Table.keys(),
            index=0,
            key=State.join_table(0),
        )
    with t1_col2:
        t1_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table1),
            placeholder="Select columns to be displayed",
            key=State.display_columns(0),
        )

    t2_col1, t2_col2 = st.columns(2)
    with t2_col1:
        table2 = st.selectbox(
            "Table 2",
            Table.keys(exclude=table1),
            index=0,
            key=State.join_table(1),
        )
    with t2_col2:
        t2_columns = st.multiselect(
            "Columns",
            repo.read_table_columns(table2),
            placeholder="Select columns to be displayed",
            key=State.display_columns(1),
        )

    st.subheader("Conditions")

    st.caption("Join condition")

    join_cond_col1, join_cond_col2 = st.columns(2)
    with join_cond_col1:
        t1_join_column = st.selectbox(
            f"{table1} join column",
            ["trade_union_id"] if table1 == Table.EMPLOYEE else ["id"],
            key=State.join_column(0),
        )
    with join_cond_col2:
        t2_join_column = st.selectbox(
            f"{table2} join column",
            ["trade_union_id"] if table2 == Table.EMPLOYEE else ["id"],
            key=State.join_column(1),
        )

    selection_condition_view()


def selection_condition_view() -> None:
    st.caption("Selection conditions")

    if State.num_conditions not in st.session_state:
        st.session_state[State.num_conditions] = 1

    condition_col1, condition_col2, condition_col3, condition_col4 = st.columns(4)

    for i in range(st.session_state[State.num_conditions]):
        with condition_col1:
            condition_type = st.selectbox(
                "Condition type",
                ["Equality", "Range"],
                key=State.condition_type(i),
            )

        with condition_col2:
            table = st.selectbox("Table", Table.keys(), key=State.condition_table(i))

        with condition_col3:
            condition_column = st.selectbox(
                "Column",
                repo.read_table_key_columns(table),
                key=State.condition_column(i),
            )

        with condition_col4:
            if condition_type == "Equality":
                st.text_input("Value", key=State.condition_value(i))
            elif condition_type == "Range":
                range_col1, range_col2 = st.columns(2)
                with range_col1:
                    st.text_input("Min", key=State.condition_min(i))
                with range_col2:
                    st.text_input("Max", key=State.condition_max(i))

    def add_condition() -> None:
        st.session_state[State.num_conditions] += 1

    st.button(
        "Add selection condition",
        on_click=lambda: add_condition(),
    )

def analyze() -> None:
    st.write(st.session_state)
    # info = QueryInfo()
    # is_join_query = st.session_state["is_join_query"]
    # if is_join_query:
    #     info.type = QueryType.JOIN
    # else:
    #     info.type = QueryType.NORMAL
        
        

main()
