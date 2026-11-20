import contextlib
from typing import Any, Generator

import streamlit as st

from app.components.alert import show_alert
from app.components.transaction_details_grid import transactions_details_grid
from app.data.models import Transaction, BankAccount, TransactionType, Category
from app.data.streamlit_state_keys import HOME_ALERT_MSG, HOME_ALERT_ICON, TRANSACTIONS_SELECTED_TRANSACTION
from app.db.database import db


def _check_can_add_transaction():
    if db.BankAccounts.empty:
        st.session_state[HOME_ALERT_MSG] = ":red[You have no accounts, create some!]"
        st.session_state[HOME_ALERT_ICON] = "🚨"
        show_alert(HOME_ALERT_MSG, HOME_ALERT_ICON)
        return False

    elif db.Categories.empty:
        st.session_state[HOME_ALERT_MSG] = ":red[You have no categories, create some!]"
        st.session_state[HOME_ALERT_ICON] = "🚨"
        show_alert(HOME_ALERT_MSG, HOME_ALERT_ICON)
        return False

    return True


@st.dialog(
    title="Create Transaction", width="medium", position="center", )
def _create_transaction_dialog(transaction: Transaction):
    transactions_details_grid(transaction)


def _open_create_transaction_dialog(selected_bank_account: BankAccount):
    default_category = Category.model_validate(db.Categories.iloc[0].to_dict())

    transaction = Transaction(
        title=default_category.name,
        amount=1,
        type=TransactionType.EXPENSE,
        category_id=default_category.id,
        account_id=selected_bank_account.id
    )

    db.save(transaction, op="add")

    st.session_state[TRANSACTIONS_SELECTED_TRANSACTION] = transaction

    _create_transaction_dialog(transaction)


def actions_col(bank_accounts: list[BankAccount]) -> BankAccount:
    col1, col2, col3 = st.columns([6, 3.5, 1.5])

    with col1:
        search = st.text_input(
            "Search",
            placeholder="Search transactions",
            label_visibility="collapsed",
            key="home_search",
        )
        # TODO: add on change do search

    with col2:
        selected_bank_account: BankAccount = st.selectbox(
            "Select a bank account",
            options=bank_accounts,
            format_func=lambda acc: acc.name,
            label_visibility="collapsed",
        )

    with col3:
        if st.button(label="Add", icon=":material/add:", width="stretch", ) and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account)

    return selected_bank_account
