import streamlit as st


def stat_container(col: st.Column, top_text: str, bottom_text: str):
    with col:
        with st.container(border=True, horizontal_alignment="center"):
            st.markdown(top_text, text_alignment="center")
            st.text(bottom_text)
