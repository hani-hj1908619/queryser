from time import sleep
import streamlit as st
from queryser.constants import QUERY_MODEL
from streamlit_extras.switch_page_button import switch_page
from queryser.builder import generate_sql_query
import pandas as pd
from queryser import analyser


def main() -> None:
    st.set_page_config(
        page_title="Optimizer",
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
        alorithms_data = {
            "Algorithm": [
                "Linear Search",
                "Binary Search",
                "Primary (B+ Tree) Index",
                "Hash Key",
                "Secondary (B+ Tree) Index",
            ],
            "Description": [
                "Searches all file blocks to retrieve all records sequentially.",
                "Searches in a sorted file using binary search based on attribute.",
                "Uses primary B+ Tree index to directly retrieve a single record.",
                "Uses hash key to directly retrieve a single record.",
                "Uses secondary index (B+ tree) to retrieve records.",
            ],
            "Cost": [
                "b [or b/2 on average]",
                "log2 (b) [or Range Query: log(b) + r]",
                "h + 1 [or Range Query: h + r]",
                "1 [Range Query: Not supported)",
                "h + 1 + s [or Range Query: h + (b/2)]",
            ],
        }
        st.table(pd.DataFrame(alorithms_data))

        st.caption("The algorithms used to execute your query are as follows:")
        st.table(analyser.get_best_algorithms(st.session_state[QUERY_MODEL]))


main()
