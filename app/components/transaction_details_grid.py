from typing import get_args
from uuid import UUID

import streamlit as st
from iso4217 import Currency

from app.data.colors import BadgeColor, color_emojis
from app.data.icons import icon_options
from app.data.models import BankAccount, TransactionView, Transaction, Category
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT, TRANSACTIONS_SELECTED_TRANSACTION
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

    def date_in():
        grid.write("Date")
        key = f"date_{transaction.id}"

        grid.date_input(
            label="Date",
            label_visibility="collapsed",
            value=transaction.date,
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
    category_in()
    date_in()
    note_in()
