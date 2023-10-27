import streamlit as st
import repo

st.set_page_config(layout="wide")
st.title("Trade Union")
st.table(repo.read_trade_union_table())