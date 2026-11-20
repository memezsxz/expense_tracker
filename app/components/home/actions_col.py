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


def _open_create_transaction_dialog(selected_bank_account: BankAccount, type: TransactionType):
    default_category = Category.model_validate(db.Categories.iloc[0].to_dict())

    transaction = Transaction(
        title=default_category.name,
        amount=1,
        type=type,
        category_id=default_category.id,
        account_id=selected_bank_account.id
    )

    db.save(transaction, op="add")

    st.session_state[TRANSACTIONS_SELECTED_TRANSACTION] = transaction

    @st.dialog(
        title=f"Create {transaction.type.value.title()}",
        width="medium",
        position="center",
    )
    def dialog():
        transactions_details_grid(transaction)

    dialog()


def actions_col(bank_accounts: list[BankAccount]) -> BankAccount:
    col1, col2, col3, col4, col5 = st.columns([4, 3, 0.7, 0.7, 0.7])

    with col1:
        st.text_input(
            "Search",
            placeholder="Search transactions",
            label_visibility="collapsed",
            key="home_search",
        )

    with col2:
        selected_bank_account: BankAccount = st.selectbox(
            "Select a bank account",
            options=bank_accounts,
            format_func=lambda acc: acc.name,
            label_visibility="collapsed",
        )

    with col3:
        if st.button("", icon=":material/trending_down:",
                     width="stretch", key="add_expense", help="Add Expense") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.EXPENSE)

    with col4:
        if st.button("", icon=":material/trending_up:",
                     width="stretch", key="add_income", help="Add Income") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.INCOME)

    with col5:
        if st.button("", icon=":material/swap_horiz:",
                     width="stretch", key="add_transfer", help="Add Transfer") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.TRANSFER)

    return selected_bank_account
