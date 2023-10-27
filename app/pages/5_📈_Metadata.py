import streamlit as st
import repo

st.set_page_config(
    page_title="Metadata",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Metadata and Statistics")
st.dataframe(data=repo.read_metadata_table())

st.dataframe(data=repo.read_table_stats())
