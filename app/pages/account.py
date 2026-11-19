import streamlit as st

from app.components.account_details_grid import details_grid
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT, ACCOUNTS_ERROR

account = st.session_state.get(ACCOUNT_SELECTED_ACCOUNT)

if not account:
    st.session_state[ACCOUNTS_ERROR] = "Could not reach account details"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))

with st.container(
    horizontal=True,
    horizontal_alignment="distribute",
    vertical_alignment="center",
    gap="small",
):
    st.title(account.name, icon=account.icon, anchor=False)

    st.button(
        "",
        type="primary",
        icon=":material/delete:",
    )
    # TODO: add delete

st.divider()

details_grid(account)

st.divider()

st.markdown("### Stats:", anchors=False)
# TODO: add stats
