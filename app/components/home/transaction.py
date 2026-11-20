import streamlit as st

from app.data.models import Transaction, TransactionView, TransactionType


def view_transaction(transaction: TransactionView):
    pass

def transaction_expandable(transaction_view: TransactionView):  # TODO: change to an expandable
    t_con = st.container(border=True)
    with t_con:  # click on to view Account page
        col1, col2, col3, col4 = st.columns([0.8, 8, 1, 0.5], vertical_alignment="center")

        with col1:
            st.badge(label="", icon=transaction_view.category.icon, color=transaction_view.category.color)

        with col2:
            st.write(transaction_view.transaction.title)

        with col3:
            color = (
                "red" if transaction_view.transaction.type == TransactionType.EXPENSE
                else "green" if transaction_view.transaction.type == TransactionType.INCOME
                else "gray"
            )

            sign = "-" if transaction_view.transaction.type == TransactionType.EXPENSE else "+" if transaction_view.transaction.type == TransactionType.INCOME else ""

            currency = transaction_view.account.currency

            st.write(
                f":{color}[{sign}{transaction_view.transaction.amount:,.{currency.exponent}f} {currency.code}]"
            )

        with col4: # TODO: make it an edit button and dialog should show delete button
            st.button("",
                      type="tertiary",
                      icon=":material/manage_search:",
                      key=f"view_btn_{transaction_view.transaction.id}",
                      on_click=view_transaction,
                      args=(transaction_view,),
                      )
