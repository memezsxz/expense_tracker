import streamlit as st

def show_missing_and_stop(message: str):
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(f":gray[{message}]",
                    text_alignment="center"
                    )
    st.stop()
