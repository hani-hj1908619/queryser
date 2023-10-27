import streamlit as st

from queryser.constants import QUERY_MODEL
from queryser.query import (
    QueryInfo,
)

def main() -> None:
    st.set_page_config(page_title="Costs", page_icon='🪙', layout="wide")
    st.title("Query Costs\n")
    
    if QUERY_MODEL not in st.session_state:
        st.error("Please select a query first", icon='❗')
        st.markdown('### Navigate to [Query Selector](./Query) 👈 ')
    else:
        query_info = QueryInfo.model_validate(st.session_state[QUERY_MODEL])
        st.write(query_info)

main()