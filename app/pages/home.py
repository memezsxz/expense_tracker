import streamlit as st

from app.components.alert import show_alert
from app.data.mock_data import mock_bank_accounts
from app.data.models import Transaction, TransactionView, BankAccount
from app.data.streamlit_state_keys import HOME_ALERT_MSG, HOME_ALERT_ICON
from app.db.database import db


def view_transaction(to_view_transaction: Transaction):
    pass


bank_accounts: list[BankAccount] = [
    BankAccount.model_validate(row)
    for row in db.BankAccounts.to_dict(orient="records")
]


col1, col2, col3 = st.columns([6, 3.5, 1.5])

with col1:
    search = st.text_input(label="collapsed", label_visibility="collapsed", placeholder="Search")
    # TODO: add on change do search

with col2:
    selected_bank_account = st.selectbox(
        "Select a bank account",
        options=bank_accounts,
        format_func=lambda acc: acc.name,
        label_visibility="collapsed",
    )

with col3:
    add_btn = st.button(label="Add", icon=":material/add:", width="stretch")

st.space(size="small")

if len(bank_accounts) == 0:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[You have no bank accounts, create some to add transactions!]",
                    text_alignment="center"
                    )
    st.stop()

if db.Transactions.empty:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[You have no transactions, create some!]",
                    text_alignment="center")
        st.stop()

print(db.Transactions.columns)

transactions: list[TransactionView] = db.get_transactions_by_account(selected_bank_account.id)

#     [
#     Transaction.model_validate(row)
#     for row in db.Transactions[db.Transactions["account_id"] == selected_bank_account.id].to_dict(orient="records")
# ]

# transactions = mock_transactions

if len(transactions) == 0:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[You have no transactions, create some!]", text_alignment="center")

for t in transactions:
    acc_con = st.container(border=True)
    with acc_con:  # click on to view Account page
        col1, col2, col3, col4 = st.columns([0.8, 8, 1, 0.5], vertical_alignment="center")

        with col1:
            # st.badge(label="", icon=t.icon, color=account.color)
            st.write("icon")

        with col2:
            st.write(t.title)

        with col3:
            # TODO: change color based on t type and add negative for expense
            st.write(t.amount)
            # TODO: add currency

        with col4:
            st.button("",
                      type="tertiary",
                      icon=":material/manage_search:",
                      key=f"view_btn_{t.id}",
                      on_click=view_transaction,
                      args=(t,),
                      )

show_alert(HOME_ALERT_MSG, HOME_ALERT_ICON)
