import os

import pandas as pd
import streamlit as st

with st.sidebar:
    selected_page = st.radio(
        "Add a radio button",
        ["home", "connect", "flash"]
    )

if selected_page == "home":
    st.title("Home")
    title = st.text_input("What did you spend on?", placeholder="Burger")

    st.write("I spent on " + title)

    st.markdown("# asdsa")

    amount = st.number_input("How old are you?", min_value=0, max_value=100, value=100)

    category = st.selectbox("Are you dead?", ["Yes", "No", "Prefer not to say"])

    if st.button("Add Expense"):
        st.write("Done")

        new_row = pd.DataFrame([[amount, category]], columns=["amount", "category"])

        if os.path.isfile("./data/export.csv"):
            new_row = pd.concat(
                [pd.read_csv("./data/export.csv"),
                 new_row],
                ignore_index=True
            )

        new_row.to_csv("data/export.csv", index=False)
        st.dataframe(new_row)
