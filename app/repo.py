from db import supabase
from postgrest import APIResponse
import pandas as pd

def read_employee_table() -> pd.DataFrame:
    res = supabase.table("employee").select("*").execute()
    return pd.DataFrame(res.data)
    
