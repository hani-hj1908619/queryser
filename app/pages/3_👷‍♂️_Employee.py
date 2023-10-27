import streamlit as st
import repo


st.set_page_config(
    page_title="Employee",
    page_icon="👷‍♂️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Employee Table")
st.dataframe(data=repo.read_employee_table(), use_container_width=True)
