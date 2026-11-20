import streamlit as st
from iso4217 import Currency

from app.components.alert import show_alert
from app.data.models import BankAccount
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT, ACCOUNTS_ALERT_ICON, ACCOUNTS_ALERT_MSG
from app.db.database import db


def view_account(to_account: BankAccount):
    st.session_state[ACCOUNT_SELECTED_ACCOUNT] = to_account
    st.switch_page(st.Page(PAGE_PATH.ACCOUNT))


def add_account_btn():
    new_account = BankAccount(
        name="Default",
        balance=0,
        color="yellow",
        icon=":material/savings:",
        currency=Currency.BHD,
    )

    db.save(new_account, op="add")

    view_account(new_account)


bank_accounts: list[BankAccount] = [
    BankAccount.model_validate(row)
    for row in db.BankAccounts.to_dict(orient="records")
]

# TODO: add paging

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

if len(bank_accounts) == 0:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[You have no accounts, create some!]", text_alignment="center")

for account in bank_accounts:
    acc_con = st.container(border=True)
    with acc_con:  # click on to view Account page
        col1, col2, col3, col4 = st.columns([0.8, 7, 2, 0.5], vertical_alignment="center")

        with col1:
            # account icon in circle of color
            st.badge(label="", icon=account.icon, color=account.color)

        with col2:
            # account name
            st.write(account.name)

        with col3:
            # current account balance
            st.write(f"{account.balance:.2f}{account.currency.code}")

        with col4:
            st.button("",
                      type="tertiary",
                      icon=":material/manage_search:",
                      key=f"view_btn_{account.id}",
                      on_click=view_account,
                      args=(account,),
                      )

show_alert(ACCOUNTS_ALERT_MSG, ACCOUNTS_ALERT_ICON)
