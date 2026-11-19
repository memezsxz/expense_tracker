import streamlit as st
from iso4217 import Currency

from app.data.mock_data import bank_accounts
from app.data.models import BankAccount
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNTS_ERROR, ACCOUNT_SELECTED_ACCOUNT
from app.db.database import db

# TODO: add retrival
accounts = bank_accounts


def add_account_btn():
    db.save(BankAccount(
        name="NBB",
        balance=0,
        color="yellow",
        icon=":material/savings:",
        currency=Currency.BHD,
    ),
        op="add"
    )


with st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
        gap="small",
):
    st.title("Manage Accounts")

    st.button(
        "Add New Account",
        type="secondary",
        icon=":material/add:",
        on_click=add_account_btn
    )

st.space(size="small")

for account in bank_accounts:
    acc_con = st.container(border=True)
    with acc_con:  # click on to view Account page
        col1, col2, col3, col4 = st.columns([0.8, 8, 1, 0.5], vertical_alignment="center")

        with col1:
            # account icon in circle of color
            st.badge(label="", icon=account.icon, color=account.color)

        with col2:
            # account name
            st.write(account.name)

        with col3:
            # current account balance
            st.write(f"{account.balance}{account.currency.code}")

        with col4:
            if st.button("", type="tertiary", icon=":material/manage_search:"):
                st.session_state[ACCOUNT_SELECTED_ACCOUNT] = account
                st.switch_page(st.Page(PAGE_PATH.ACCOUNT))

error_msg = st.session_state.get(ACCOUNTS_ERROR)
if error_msg:
    st.toast(f":red[{error_msg}]", icon="🚨")
    st.session_state[ACCOUNTS_ERROR] = None
