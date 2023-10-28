from time import sleep
import streamlit as st
from queryser.query import QueryInfo, QueryType, EqualityFilter, RangeFilter
from queryser.constants import QUERY_MODEL
from streamlit_extras.switch_page_button import switch_page


def main() -> None:
    st.set_page_config(
        page_title="Algorithms",
        page_icon="��🖥️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Query Algorithms")

    if QUERY_MODEL not in st.session_state:
        st.error("Please select a query first", icon='❗')
        with st.spinner("Redirecting to Query page..."):
            sleep(1.5)
            switch_page("Query")

    else:
        st.subheader("SQL Query")

        query_model: QueryInfo = st.session_state[QUERY_MODEL]
        model_dump = (
            query_model.simple.model_dump()
            if query_model.simple
            else query_model.join.model_dump()
        )
        st.write(model_dump)

        st.markdown(
            f"""
            ```sql
           {generate_sql_query(st.session_state[QUERY_MODEL])}
            ```
            """
        )

        st.write()

        st.subheader("Algorithms")
        st.caption("The algorithms used to execute your query are as follows:")


def generate_sql_query(query_info: QueryInfo) -> str:
    if query_info.type == QueryType.NORMAL:
        table_name = query_info.simple.table.name

        res_attrs = (
            ", ".join(query_info.simple.res_attrs)
            if query_info.simple.res_attrs
            else "*"
        )

        where_clauses = []
        for filter_clause in query_info.simple.where_attrs:
            if isinstance(filter_clause, EqualityFilter):
                operator = "!=" if filter_clause.negated else "="
                where_clauses.append(
                    f"{filter_clause.column} {operator} {filter_clause.value}"
                )
            elif isinstance(filter_clause, RangeFilter):
                if filter_clause.min_value and filter_clause.max_value:
                    where_clauses.append(
                        f"{filter_clause.column} BETWEEN ({filter_clause.min_value} AND {filter_clause.max_value})"
                    )
                elif filter_clause.min_value:
                    where_clauses.append(
                        f"{filter_clause.column} >= {filter_clause.min_value}"
                    )
                elif filter_clause.max_value:
                    where_clauses.append(
                        f"{filter_clause.column} <= {filter_clause.max_value}"
                    )

        where_clause = " AND ".join(where_clauses)
        if where_clause:
            sql_query = f"SELECT {res_attrs} FROM {table_name} WHERE {where_clause};"
        else:
            sql_query = f"SELECT {res_attrs} FROM {table_name};"

    elif query_info.type == QueryType.JOIN:
        # Handle JOIN queries here
        table1_name = query_info.join.table_1_query.table.name
        table2_name = query_info.join.table_2_query.table.name
        table1_attrs = ", ".join(
            query_info.join.table_1_query.res_attrs) if query_info.join.table_1_query.res_attrs else "*"
        table2_attrs = ", ".join(
            query_info.join.table_2_query.res_attrs) if query_info.join.table_2_query.res_attrs else "*"

        where_clauses = []
        # Add WHERE clauses for table 1 conditions
        for filter_clause in query_info.join.table_1_query.where_attrs:
            if isinstance(filter_clause, EqualityFilter):
                operator = "!=" if filter_clause.negated else "="
                where_clauses.append(
                    f"{table1_name}.{filter_clause.column} {operator} {filter_clause.value}"
                )
            elif isinstance(filter_clause, RangeFilter):
                if filter_clause.min_value and filter_clause.max_value:
                    where_clauses.append(
                        f"{table1_name}.{filter_clause.column} BETWEEN {filter_clause.min_value} AND {filter_clause.max_value}"
                    )
                elif filter_clause.min_value:
                    where_clauses.append(
                        f"{table1_name}.{filter_clause.column} >= {filter_clause.min_value}"
                    )
                elif filter_clause.max_value:
                    where_clauses.append(
                        f"{table1_name}.{filter_clause.column} <= {filter_clause.max_value}"
                    )

        # Add WHERE clauses for table 2 conditions
        for filter_clause in query_info.join.table_2_query.where_attrs:
            if isinstance(filter_clause, EqualityFilter):
                operator = "!=" if filter_clause.negated else "="
                where_clauses.append(
                    f"{table2_name}.{filter_clause.column} {operator} {filter_clause.value}"
                )
            elif isinstance(filter_clause, RangeFilter):
                if filter_clause.min_value and filter_clause.max_value:
                    where_clauses.append(
                        f"{table2_name}.{filter_clause.column} BETWEEN {filter_clause.min_value} AND {filter_clause.max_value}"
                    )
                elif filter_clause.min_value:
                    where_clauses.append(
                        f"{table2_name}.{filter_clause.column} >= {filter_clause.min_value}"
                    )
                elif filter_clause.max_value:
                    where_clauses.append(
                        f"{table2_name}.{filter_clause.column} <= {filter_clause.max_value}"
                    )

        # Add JOIN condition
        join_condition = f"{table1_name}.{query_info.join.table_1_attr} = {table2_name}.{query_info.join.table_2_attr}"

        where_clause = " AND ".join(where_clauses)
        if where_clause:
            sql_query = f"SELECT {table1_attrs}, {table2_attrs} FROM {table1_name} JOIN {table2_name} ON {join_condition} WHERE {where_clause};"
        else:
            sql_query = f"SELECT {table1_attrs}, {table2_attrs} FROM {table1_name} JOIN {table2_name} ON {join_condition};"

    else:
        raise ValueError("Invalid query type")
    return sql_query


main()
