import streamlit as st

    
st.set_page_config(
    page_title="Queryser",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded",
)


def home():
    st.title("Welcome to Queryser 🚀")
    st.markdown("## A simple tool to analyze sql queries")
    st.info("👈 Queryser currently only suports simple select andf equijoin queries over keys")


home()

