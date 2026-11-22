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


def _open_create_transaction_dialog(
        selected_bank_account: BankAccount,
        type: TransactionType
):
    category_id = None
    to_account_id = None
    title = "Transfer"

    if type == TransactionType.TRANSFER:
        accounts = [
            BankAccount.model_validate(row)
            for row in db.BankAccounts.to_dict("records")
        ]

        other_account = next(
            (
                a for a in accounts
                if a.id != selected_bank_account.id
                   and a.currency == selected_bank_account.currency
            ),
            None
        )

        if other_account is None:
            st.session_state[HOME_ALERT_MSG] = ":red[You have no other account with the same currency!]"
            st.session_state[HOME_ALERT_ICON] = ""
            show_alert(HOME_ALERT_MSG, HOME_ALERT_ICON)
            return

        to_account_id = other_account.id

    else:
        default_category = Category.model_validate(
            db.Categories.iloc[0].to_dict()
        )

        category_id = default_category.id
        title = default_category.name

    transaction = Transaction(
        title=title,
        amount=1,
        type=type,
        category_id=category_id,
        account_id=selected_bank_account.id,
        to_account_id=to_account_id,
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
    categories: list[Category] = [
        Category.model_validate(row)
        for row in db.Categories.to_dict(orient="records")
    ]

    col1, col2, col3, col4, col5, col6 = st.columns([2.5, 2.5, 2, 0.7, 0.7, 0.7])

    with col1:
        st.text_input(
            "Search",
            placeholder="Search transactions",
            label_visibility="collapsed",
            key="home_search",
        )

    with col2:
        selected_bank_account = st.selectbox(
            "Select a bank account",
            options=bank_accounts,
            format_func=lambda acc: f"{acc.name} ({str(acc.id)[:6]})",
            label_visibility="collapsed",
            key="home_select_account",
        )

    with col3:
        selected_category = st.selectbox(
            "Select category",
            options=[None] + categories,
            format_func=lambda cat: (
                "No category" if cat is None
                else f"{cat.name} ({str(cat.id)[:6]})"
            ),
            label_visibility="collapsed",
            key="home_select_category",
        )

    with col4:
        if st.button("", icon=":material/trending_down:",
                     width="stretch", key="add_expense", help="Add Expense") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.EXPENSE)

    with col5:
        if st.button("", icon=":material/trending_up:",
                     width="stretch", key="add_income", help="Add Income") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.INCOME)

    with col6:
        if st.button("", icon=":material/swap_horiz:",
                     width="stretch", key="add_transfer", help="Add Transfer") and _check_can_add_transaction():
            _open_create_transaction_dialog(selected_bank_account, TransactionType.TRANSFER)

    return selected_bank_account, selected_category
