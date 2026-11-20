import datetime
from uuid import UUID

import streamlit as st

from app.data.models import BankAccount, Transaction, TransactionType
from app.data.streamlit_state_keys import TRANSACTIONS_SELECTED_TRANSACTION
from app.db.database import db


def update_transaction(field: str, widget_key: str):
    current = st.session_state[TRANSACTIONS_SELECTED_TRANSACTION]

    copy = current.model_copy(
        update={field: st.session_state[widget_key]}
    )

    st.session_state[TRANSACTIONS_SELECTED_TRANSACTION] = copy
    db.save(copy, op="edit")


def transactions_details_grid(
        transaction: Transaction,
):
    transaction = st.session_state[TRANSACTIONS_SELECTED_TRANSACTION]

    categories = {
        UUID(str(row["id"])): row
        for row in db.Categories.to_dict("records")
    }

    selected_category = categories.get(transaction.category_id)

    grid = st.grid(2, vertical_alignment="center")

    def title_in():
        grid.write("Title")
        key = f"title_{transaction.id}"

        grid.text_input(
            label="Title",
            label_visibility="collapsed",
            value=transaction.title,
            key=key,
            on_change=update_transaction,
            args=("title", key),
        )

    def amount_in():
        grid.write("Amount")
        key = f"amount_{transaction.id}"

        grid.number_input(
            label="Amount",
            label_visibility="collapsed",
            value=transaction.amount,
            min_value=0.001,
            max_value=10_000_000.0,
            step=1.0,
            key=key,
            on_change=update_transaction,
            args=("amount", key),
        )

    def category_in():
        with grid.container(
                horizontal=True,
                vertical_alignment="center",
                gap="xsmall"
        ):
            st.write("Category")
            st.badge("", icon=selected_category["icon"], color=selected_category["color"])

        with grid.cell():
            key = f"category_{transaction.id}"
            ids = list(categories)

            st.selectbox(
                "Category",
                options=ids,
                format_func=lambda id: categories[id]["name"],
                index=(
                    ids.index(transaction.category_id)
                    if transaction.category_id in ids
                    else None
                ),
                key=key,
                on_change=update_transaction,
                args=("category_id", key),
                label_visibility="collapsed",
            )

    def to_account_in():
        grid.write("To Account")

        with grid.cell():
            accounts = [
                BankAccount.model_validate(row)
                for row in db.BankAccounts.to_dict("records")
            ]

            accounts = [
                a for a in accounts
                if a.id != transaction.account_id
            ]

            account_ids = [a.id for a in accounts]
            account_names = {a.id: a.name for a in accounts}

            key = f"to_account_{transaction.id}"

            st.selectbox(
                "To Account",
                options=account_ids,
                format_func=lambda id: account_names[id],
                index=(
                    account_ids.index(transaction.to_account_id)
                    if transaction.to_account_id in account_ids
                    else None
                ),
                label_visibility="collapsed",
                key=key,
                on_change=update_transaction,
                args=("to_account_id", key),
            )

    def date_in():
        grid.write("Date")
        key = f"date_{transaction.id}"

        grid.date_input(
            label="Date",
            label_visibility="collapsed",
            value=transaction.date,
            max_value=datetime.date.today(),
            key=key,
            on_change=update_transaction,
            args=("date", key),
        )

    def note_in():
        grid.write("Notes")
        key = f"notes_{transaction.id}"

        grid.text_area(
            label="Notes",
            label_visibility="collapsed",
            value=transaction.notes,
            key=key,
            on_change=update_transaction,
            args=("notes", key),
        )

    title_in()
    amount_in()

    if transaction.type == TransactionType.TRANSFER:
        to_account_in()
    else:
        category_in()

    date_in()
    note_in()
