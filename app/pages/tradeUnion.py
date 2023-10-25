import streamlit as st
import repo
df = repo.read_trade_union_table()


st.set_page_config(
    page_title="Trade Union",
    page_icon="🪣",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Trade Union")
st.table(df)
st.sidebar.markdown("The Trade Union data")
st.write("Table Info")
st.write("Number of trade unions: " , len(df))
