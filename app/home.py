from collections import namedtuple
import math
import pandas as pd
import streamlit as st
import enum
import queryser

    
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

    query = st.text_area(
        "Insert Query",
        value="",
        label_visibility="hidden",
        placeholder="SELECT NAME FROM EMPLOYEE",
        key=QueryserState.QUERY,
    )

    if query and queryser.tokenizer.validate_sql(query):
        st.button("Analyze")
    
    
class QueryserState(enum.StrEnum):
    QUERY = enum.auto()

home()

