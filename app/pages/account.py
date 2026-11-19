
import streamlit as st

from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT_ID, ACCOUNTS_ERROR

account_id = st.session_state.get(ACCOUNT_SELECTED_ACCOUNT_ID)

if not account_id:
    st.session_state[ACCOUNTS_ERROR] = "Could not reach account details"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))

st.title(account_id)