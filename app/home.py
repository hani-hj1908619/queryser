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

home()