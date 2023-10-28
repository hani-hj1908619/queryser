import streamlit as st
import repo
from queryser.constants import QUERY_MODEL, Table
from queryser.query import (
    JoinQueryInfo,
    SimpleQueryInfo,
    RangeFilter,
    EqualityFilter,
    QueryInfo,
    QueryType,
)
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
    def join_column(cls, i: int | None = None) -> str:
        return f"join_column_{i}" if i is not None else "join_column"

    @classmethod
    def condition_type(cls, i: int | None = None) -> str:
        return f"condition_type_{i}" if i is not None else "condition_type"

    @classmethod
    def condition_table(cls, i: int | None = None) -> str:
        return f"condition_table_{i}" if i is not None else "condition_table"

    @classmethod
    def condition_column(cls, i: int | None = None) -> str:
        return f"condition_column_{i}" if i is not None else "condition_column"

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
    st.set_page_config(page_title="Query", page_icon="📝", layout="wide")

    st.subheader("Select")

    is_join_query = st.checkbox(
        "Is equi-join query",
        key=State.is_join_query,
        value=False,
    )
    if is_join_query:
        join_query_view()
    else:
        normal_query_view()

    st.button("Analyse", on_click=analyze)


def normal_query_view() -> None:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        table = st.selectbox("Table", Table.keys(), index=0, key=State.select_table)
    with t1_col2:
        st.multiselect(
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
        st.multiselect(
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
        st.multiselect(
            "Columns",
            repo.read_table_columns(table2),
            placeholder="Select columns to be displayed",
            key=State.display_columns(1),
        )

    st.subheader("Conditions")

    st.caption("Join condition")

    join_cond_col1, join_cond_col2 = st.columns(2)
    with join_cond_col1:
        st.selectbox(
            f"{table1} join column",
            ["trade_union_id"] if table1 == Table.EMPLOYEE else ["id"],
            key=State.join_column(0),
        )
    with join_cond_col2:
        st.selectbox(
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
                ["Equal", "Not Equal", "Range"],
                key=State.condition_type(i),
            )

        with condition_col2:
            table = st.selectbox(
                "Table",
                Table.keys()
                if st.session_state[State.is_join_query]
                else [st.session_state[State.select_table]],
                key=State.condition_table(i),
            )

        with condition_col3:
            st.selectbox(
                "Column",
                repo.read_table_key_columns(table),
                key=State.condition_column(i),
            )

        with condition_col4:
            if condition_type == "Equal" or condition_type == "Not Equal":
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
    if st.session_state[State.is_join_query]:
        query_info = JoinQueryInfo(
            table_1_query=SimpleQueryInfo(
                table=Table(st.session_state[State.join_table(0)]),
                res_attrs=st.session_state[State.display_columns(0)],
            ),
            table_2_query=SimpleQueryInfo(
                table=Table(st.session_state[State.join_table(1)]),
                res_attrs=st.session_state[State.display_columns(1)],
            ),
            table_1_attr=st.session_state[State.join_column(0)],
            table_2_attr=st.session_state[State.join_column(1)],
        )

        for i in range(st.session_state[State.num_conditions]):
            filter = generate_filter(i)

            if filter:
                table = st.session_state[State.condition_table(i)]
                if table == st.session_state[State.join_table(0)]:
                    query_info.table_1_query.where_attrs.append(filter)
                elif table == st.session_state[State.join_table(1)]:
                    query_info.table_2_query.where_attrs.append(filter)
    else:
        query_info = SimpleQueryInfo(
            table=Table(st.session_state[State.select_table]),
            res_attrs=st.session_state[State.display_columns()],
        )

        for i in range(st.session_state[State.num_conditions]):
            filter = generate_filter(i)
            if filter:
                query_info.where_attrs.append(filter)

    is_join_query = st.session_state[State.is_join_query]
    st.session_state.clear()
    st.session_state[QUERY_MODEL] = QueryInfo(
        type=QueryType.JOIN if is_join_query else QueryType.NORMAL,
        simple=query_info if not is_join_query else None,
        join=query_info if is_join_query else None,
    )

    st.success("Query model created successfully", icon="✅")
    st.markdown(
        """
        Navigate to [Query Optimizer](./Optimizer) 👈 to learn more about query optimizer\
        
        
        Navigate to [Costs](./Cost) 👈 to learn more about costs for different excution plans
    """
    )


def generate_filter(condition_number: int):
    condition_type = st.session_state[State.condition_type(condition_number)]
    table = st.session_state[State.condition_table(condition_number)]

    filter = None
    if condition_type == "Equal" or condition_type == "Not Equal":
        if st.session_state[State.condition_value(condition_number)]:
            filter = EqualityFilter(
                column=st.session_state[State.condition_column(condition_number)],
                value=st.session_state[State.condition_value(condition_number)],
                negated=condition_type == "Not Equal",
            )
    elif condition_type == "Range":
        if (
            st.session_state[State.condition_min(condition_number)]
            or st.session_state[State.condition_max(condition_number)]
        ):
            filter = RangeFilter(
                column=st.session_state[State.condition_column(condition_number)],
                min_value=st.session_state[State.condition_min(condition_number)]
                or None,
                max_value=st.session_state[State.condition_max(condition_number)]
                or None,
            )

    return filter


main()
