import pydantic
from db import supabase
import pandas as pd
from functools import lru_cache
from queryser import constants


@lru_cache
def read_metadata_table() -> pd.DataFrame:
    res = supabase.table("metadata").select("*").execute()
    return pd.DataFrame(res.data)


@lru_cache
def read_employee_table() -> pd.DataFrame:
    res = supabase.table("employee").select("*").execute()
    return pd.DataFrame(res.data)


@lru_cache
def read_trade_union_table() -> pd.DataFrame:
    res = supabase.table("trade_union").select("*").execute()
    return pd.DataFrame(res.data)


def read_table_columns(table: constants.Table) -> list:
    if table == constants.Table.EMPLOYEE:
        return read_employee_table_columns()
    elif table == constants.Table.TRADE_UNION:
        return read_trade_union_table_columns()
    else:
        raise ValueError(f"Invalid table {table}")


def read_table_key_columns(table: constants.Table) -> list:
    if table == constants.Table.EMPLOYEE:
        return read_employee_key_columns()
    elif table == constants.Table.TRADE_UNION:
        return read_trade_union_key_columns()
    else:
        raise ValueError(f"Invalid table {table}")


@lru_cache
def read_employee_table_columns() -> list:
    res = (
        supabase.table("metadata")
        .select("column_name")
        .eq("table_name", "employee")
        .execute()
    )
    return [row["column_name"] for row in res.data]


@lru_cache
def read_employee_key_columns() -> list:
    res = (
        supabase.table("metadata")
        .select("column_name")
        .eq("table_name", "employee")
        .eq("is_unique", True)
        .order("index_type")
        .execute()
    )
    return [row["column_name"] for row in res.data]


@lru_cache
def read_trade_union_table_columns() -> list:
    res = (
        supabase.table("metadata")
        .select("column_name")
        .eq("table_name", "trade_union")
        .execute()
    )
    return [row["column_name"] for row in res.data]


@lru_cache
def read_trade_union_key_columns() -> list:
    res = (
        supabase.table("metadata")
        .select("column_name")
        .eq("table_name", "trade_union")
        .eq("is_unique", True)
        .order("index_type")
        .execute()
    )
    return [row["column_name"] for row in res.data]


def read_employee_count() -> int:
    res = supabase.table("employee").select("ssn", count="exact").execute()
    return res.count


def read_trade_union_count() -> int:
    res = supabase.table("trade_union").select("id", count="exact").execute()
    return res.count


def read_table_stats() -> list:
    employee_count = read_employee_count()
    trade_union_count = read_trade_union_count()

    return pd.DataFrame(
        {
            "Table": ["employee", "trade_union"],
            "Rows": [employee_count, trade_union_count],
            "Blocks": [employee_count, trade_union_count],
        }
    )


class ColumnStats(pydantic.BaseModel):
    index_type: constants.IndexType | None
    is_unique: bool

def read_column_stats(table: constants.Table, column: str) -> ColumnStats:
    metadata = read_metadata_table()
    metadata = metadata.loc[metadata["table_name"] == table.value.lower()]
    metadata = metadata.loc[metadata["column_name"] == column]
    index_type = metadata["index_type"].values[0]
    return ColumnStats(
        index_type=constants.IndexType(index_type) if index_type else None,
        is_unique=True if metadata["is_unique"].values[0] == "True" else False,
    )

def read_trade_union_ids():
    res = supabase.table("trade_union").select("id").execute()
    return [row["id"] for row in res.data]

#function to insert employee table data
def insert_employee_data(data):
    supabase.table('employee').insert(data).execute()
def insert_trade_union_data(data):
    supabase.table('trade_union').insert(data).execute()
