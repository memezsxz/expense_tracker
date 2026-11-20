import streamlit as st

from app.components.transaction_details_grid import transactions_details_grid
from app.data.models import TransactionView, TransactionType
from app.data.streamlit_state_keys import TRANSACTIONS_SELECTED_TRANSACTION
from app.db.database import db


def view_transaction(view: TransactionView):
    st.session_state[TRANSACTIONS_SELECTED_TRANSACTION] = view.transaction

    @st.dialog(
        title=f"Edit {view.transaction.type.value.title()}",
        width="medium",
        on_dismiss="rerun",
    )
    def edit_dialog():
        transaction = st.session_state[TRANSACTIONS_SELECTED_TRANSACTION]

        transactions_details_grid(transaction)

        st.divider()

        col1, col2 = st.columns(2, vertical_alignment="bottom")

        with col1:
            confirm_delete = st.checkbox(
                "Confirm deletion",
                key=f"confirm_delete_{transaction.id}",
            )

        with col2:
            if st.button(
                "Delete",
                icon=":material/delete:",
                type="primary",
                disabled=not confirm_delete,
                width="stretch",
            ):
                db.save(transaction, op="delete")
                st.session_state.pop(TRANSACTIONS_SELECTED_TRANSACTION, None)
                st.rerun()

    edit_dialog()

def transaction_expandable(transaction_view: TransactionView):  # TODO: change to an expandable
    t_con = st.container(border=True)
    with t_con:  # click on to view Account page
        col1, col2, col3, col4 = st.columns([0.8, 7.5, 1.5, 0.5], vertical_alignment="center")

        with col1:
            category = transaction_view.category

            st.badge(
                label="",
                icon=category.icon if category else ":material/swap_horiz:",
                color=category.color if category else "blue",
            )

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

        with col4:  # TODO: make it an edit button and dialog should show delete button
            st.button("",
                      type="tertiary",
                      icon=":material/manage_search:",
                      key=f"view_btn_{transaction_view.transaction.id}",
                      on_click=view_transaction,
                      args=(transaction_view,),
                      )
