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
