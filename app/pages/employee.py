import streamlit as st
import repo

st.title("Employee Table")
st.dataframe(data=repo.read_employee_table())
