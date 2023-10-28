from queryser.query import QueryInfo, QueryType, EqualityFilter, RangeFilter


def generate_sql_query(query_info: QueryInfo) -> str:
    if query_info.type == QueryType.NORMAL:
        res_attrs = (
            ", ".join(query_info.simple.res_attrs)
            if query_info.simple.res_attrs
            else "*"
        )

        where_clauses = []
        for filter_clause in query_info.simple.where_attrs:
            where_clauses.append(generate_where_clause(filter_clause))

        sql_query = f"SELECT {res_attrs} FROM {query_info.simple.table.name}"

        where_clause = " AND ".join(where_clauses)
        sql_query += f" WHERE {where_clause};" if where_clause else ";"

    elif query_info.type == QueryType.JOIN:
        table1_name = query_info.join.table_1_query.table.name
        table2_name = query_info.join.table_2_query.table.name

        select_clause = ""
        if not (
            query_info.join.table_1_query.res_attrs
            or query_info.join.table_2_query.res_attrs
        ):
            select_clause = "*"
        else:
            if query_info.join.table_1_query.res_attrs:
                prefixed_res_attrs = [
                    f"{table1_name}.{attr}"
                    for attr in query_info.join.table_1_query.res_attrs
                ]
                select_clause += ", ".join(prefixed_res_attrs)
            else:
                select_clause += f"{table1_name}.*"

            select_clause += ", "

            if query_info.join.table_2_query.res_attrs:
                prefixed_res_attrs = [
                    f"{table2_name}.{attr}"
                    for attr in query_info.join.table_2_query.res_attrs
                ]
                select_clause += ", ".join(prefixed_res_attrs)
            else:
                select_clause += f"{table2_name}.*"

        where_clauses = []
        # Add WHERE clauses for table 1 conditions
        for filter_clause in query_info.join.table_1_query.where_attrs:
            where_clauses.append(generate_where_clause(filter_clause, table1_name))

        # Add WHERE clauses for table 2 conditions
        for filter_clause in query_info.join.table_2_query.where_attrs:
            where_clauses.append(generate_where_clause(filter_clause, table2_name))

        join_condition = f"{table1_name}.{query_info.join.table_1_attr} = {table2_name}.{query_info.join.table_2_attr}"
        sql_query = f"SELECT {select_clause} FROM {table1_name} JOIN {table2_name} ON {join_condition}"

        where_clause = " AND ".join(where_clauses)
        sql_query += f" WHERE {where_clause};" if where_clause else ";"

    else:
        raise ValueError("Invalid query type")
    return sql_query


def generate_where_clause(
    filter_clause: EqualityFilter | RangeFilter, table_name: str = ""
) -> str:
    where_clause = ""

    if table_name:
        table_name += "."

    if isinstance(filter_clause, EqualityFilter):
        operator = "!=" if filter_clause.negated else "="
        where_clause = (
            f"{table_name or ''}{filter_clause.column} {operator} {filter_clause.value}"
        )

    elif isinstance(filter_clause, RangeFilter):
        if filter_clause.min_value and filter_clause.max_value:
            where_clause = f"{table_name or ''}{filter_clause.column} BETWEEN ({filter_clause.min_value} AND {filter_clause.max_value})"
        elif filter_clause.min_value:
            where_clause = (
                f"{table_name or ''}{filter_clause.column} >= {filter_clause.min_value}"
            )
        elif filter_clause.max_value:
            where_clause = (
                f"{table_name or ''}{filter_clause.column} <= {filter_clause.max_value}"
            )
    else:
        raise ValueError("Unhandled filter type")

    return where_clause