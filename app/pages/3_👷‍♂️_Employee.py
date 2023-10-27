import streamlit as st
import repo

st.set_page_config(layout="wide")
st.title("Employee Table")
st.dataframe(data=repo.read_employee_table())
