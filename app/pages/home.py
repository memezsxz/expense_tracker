import streamlit as st

col1, col2 = st.columns([5, 1])

with col1:
    search = st.text_input(label="collapsed",label_visibility="collapsed",  placeholder="Search")
    # add on change

with col2:
    add_btn = st.button(label="Add", icon=":material/add:")
