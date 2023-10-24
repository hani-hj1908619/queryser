from collections import namedtuple
import math
import pandas as pd
import streamlit as st

import repo

st.set_page_config(
    page_title="Queryser",
    page_icon="🪣",
    layout="wide",
    initial_sidebar_state="expanded",
)


def home():
    st.title("Queryser")
    st.sidebar.title("Queryser")
    st.sidebar.markdown("Queryser is a tool for analyzing sql queries.")

    st.markdown(
        """
        Please note that only the following type of queries are supported currently:  
          1. SELECT using a primary key with equality/range.
          2. SELECT using a non-primary key with equality/range.
          3. Only equi-joins are supported.
        """
    )

    st.header("Enter SQL Query")
    sql_query = st.text_input(
        "",
        value="",
        on_change=None,
        placeholder="SELECT NAME FROM EMPLOYEE",
    )

    if sql_query:
        st.markdown("The current query is **{}**".format(sql_query))


home()
