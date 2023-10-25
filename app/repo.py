from db import supabase
from postgrest import APIResponse
import pandas as pd

def read_employee_table() -> pd.DataFrame:
    res = supabase.table("employee").select("*").execute()
    return pd.DataFrame(res.data)
    
def read_trade_union_table() -> pd.DataFrame:
    res = supabase.table("trade_union").select("*").execute()
    return pd.DataFrame(res.data)
    