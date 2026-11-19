import streamlit as st

def show_alert(msg_key: str, icon_key: str):
    alert_msg = st.session_state.get(msg_key)
    alert_icon = st.session_state.get(icon_key)
    if alert_msg:
        st.toast(alert_msg, icon=alert_icon)
        st.session_state[msg_key] = None
        st.session_state[icon_key] = None

