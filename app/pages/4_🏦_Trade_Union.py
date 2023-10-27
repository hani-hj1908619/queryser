import streamlit as st
import repo

st.set_page_config(
    page_title="Trade Union",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Trade Union Table")
st.table(repo.read_trade_union_table())