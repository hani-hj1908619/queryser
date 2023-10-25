import streamlit as st

employee_columns = [
    "ssn",
    "email",
    "phone_number",
    "fname",
    "minit",
    "lname",
    "birth_date",
    "sex",
    "address",
    "join_date",
    "job_type",
    "typing_speed",
    "tgrade",
    "eng_type",
    "pay_type",
    "salary",
    "pay_scale",
    "trade_union_id",
]

employee_key_columns = ["ssn", "email", "phone_number"]
trade_union_columns = ["id", "name"]
trade_union_key_columns = ["id"]

st.subheader("Select")

# Main table
query_has_join = st.checkbox("Query has equi-join", value=False)

t1_col1, t1_col2 = st.columns(2)
with t1_col1:
    table1 = st.selectbox("Table 1", ["EMPLOYEE", "TRADE_UNION"])
with t1_col2:
    t1_columns = st.multiselect(
        "Columns",
        employee_columns if table1 == "EMPLOYEE" else trade_union_columns,
        placeholder="Select columns to be displayed",
    )

# Join table
if query_has_join:
    t2_col1, t2_col2 = st.columns(2)
    with t2_col1:
        table2 = st.selectbox(
            "Table 2", list(set(["EMPLOYEE", "TRADE_UNION"]) - set([table1]))
        )

    with t2_col2:
        t2_columns = st.multiselect(
            "Columns",
            employee_columns if table2 == "EMPLOYEE" else trade_union_columns,
            placeholder="Select columns to be displayed",
        )

# Condition
st.subheader("Conditions")

if query_has_join:
    st.caption("Join condition")
    join_cond_col1, join_cond_col2 = st.columns(2)

    with join_cond_col1:
        t1_join_column = st.selectbox(
            f"{table1} join column",
            ["trade_union_id"] if table1 == "EMPLOYEE" else ["id"],
        )
    with join_cond_col2:
        t2_join_column = st.selectbox(
            f"{table2} join column",
            ["trade_union_id"] if table2 == "EMPLOYEE" else ["id"],
        )

st.caption("Selection condition")

condition_col1, condition_col2, condition_col3 = st.columns(3)

with condition_col1:
    condition_type = st.selectbox("Condition type", ["Equality", "Range"])

if condition_type == "Equality":
    with condition_col2:
        condition_column = st.selectbox(
            "Column",
            employee_key_columns if table1 == "EMPLOYEE" else trade_union_key_columns,
        )
    with condition_col3:
        st.text_input("Value")

st.button("Add selection condition")
