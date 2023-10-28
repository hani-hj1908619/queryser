from time import sleep
import streamlit as st
from queryser.constants import QUERY_MODEL
from streamlit_extras.switch_page_button import switch_page
from queryser.builder import generate_sql_query


def main() -> None:
    st.set_page_config(
        page_title="Algorithms",
        page_icon="��🖥️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Query Algorithms")

    if QUERY_MODEL not in st.session_state:
        st.error("Please select a query first", icon="❗")
        with st.spinner("Redirecting to Query page..."):
            sleep(1.5)
            switch_page("Query")

    else:
        st.subheader("SQL Query")

        st.markdown(
            f"""
            ```sql
           {generate_sql_query(st.session_state[QUERY_MODEL])}
            ```
            """
        )

        st.write()

        st.subheader("Algorithms")
        st.caption("The algorithms used to execute your query are as follows:")


main()
