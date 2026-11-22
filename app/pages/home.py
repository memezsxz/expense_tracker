import datetime
from collections import defaultdict

import streamlit as st

from app.components.alert import show_alert
from app.components.home.actions_col import actions_col
from app.components.home.date_cols import change_month_col
from app.components.home.transaction import transaction_expandable
from app.components.show_missing import show_missing_and_stop
from app.data.models import TransactionView, BankAccount
from app.data.streamlit_state_keys import HOME_ALERT_MSG, HOME_ALERT_ICON, HOME_SELECTED_MONTH
from app.db.database import db
from app.utils.home_utils import get_monthly_spending

date = datetime.datetime.now()

if HOME_SELECTED_MONTH not in st.session_state:
    st.session_state[HOME_SELECTED_MONTH] = date.today().replace(day=1)

bank_accounts: list[BankAccount] = [
    BankAccount.model_validate(row)
    for row in db.BankAccounts.to_dict(orient="records")
]

selected_bank_account, selected_category = actions_col(bank_accounts)

if len(bank_accounts) == 0:
    show_missing_and_stop("You have no bank accounts, create some to add transactions!")

if selected_bank_account is None:
    show_missing_and_stop("Please select a bank account to view its transactions!")

search = st.session_state.get("home_search", "").strip()

selected_month = change_month_col()

monthly_spending = get_monthly_spending(selected_bank_account, selected_month)

budget = selected_bank_account.monthly_limit

if budget > 0:
    if monthly_spending > budget:
        st.error("You have exceeded your monthly limit!")
    elif monthly_spending >= budget * 0.9:
        st.warning("You have used 90% or more of your monthly limit!")

if db.Transactions.empty:
    show_missing_and_stop("You have no transactions, create some!")

transactions: list[TransactionView] = (
    db.get_transactions_by_account_and_month(
        selected_bank_account.id,
        selected_month.year,
        selected_month.month,
    )
)

if selected_category is not None:
    transactions = [
        t for t in transactions if t.transaction.category_id == selected_category.id
    ]

    if len(transactions) <= 0:
        show_missing_and_stop("You have no transactions, in this category, create some!")

if search:
    transactions = [
        t for t in transactions
        if search.casefold() in t.transaction.title.casefold()
           or (
                   t.category is not None
                   and search.casefold() in t.category.name.casefold()
           )
    ]

if not transactions:
    show_missing_and_stop("No transactions found for {selected_month:%B} of {selected_month.year}]")

days = defaultdict(list)

for t in transactions:
    days[t.transaction.date].append(t)

for day in sorted(days, reverse=True):
    st.divider()
    st.markdown("##### " + day.strftime("%A, %d %B"), anchors=False)

    for t in days[day]:
        transaction_expandable(t)

show_alert(HOME_ALERT_MSG, HOME_ALERT_ICON)
