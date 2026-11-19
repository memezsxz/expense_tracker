import streamlit as st
from app.db.database import db
from app.components.account_details_grid import details_grid
from app.data.models import BankAccount
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT, ACCOUNTS_ALERT_MSG, ACCOUNTS_ALERT_ICON

account = BankAccount.model_validate(st.session_state.get(ACCOUNT_SELECTED_ACCOUNT))

if not account:
    error_msg = "Could not reach account details"
    st.session_state[ACCOUNTS_ALERT_MSG] = f":red[{error_msg}]"
    st.session_state[ACCOUNTS_ALERT_ICON] = "🚨"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))

def delete_account(to_delete_account: BankAccount):
    db.save(to_delete_account, "delete")
    success_msg = "Account Deleted Successfully"
    st.session_state[ACCOUNTS_ALERT_MSG] = f":green[{success_msg}]"
    st.session_state[ACCOUNTS_ALERT_ICON] = "✅"

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
        on_click=lambda: delete_account(account),
    )
    # TODO: add delete

st.divider()

details_grid(account)

st.divider()

st.markdown("### Stats:", anchors=False)
# TODO: add stats
