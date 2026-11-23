from typing import get_args

import streamlit as st
from iso4217 import Currency

from app.data.colors import BadgeColor, color_emojis
from app.data.icons import icon_options
from app.data.models import BankAccount
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT
from app.db.database import db


def update_account(field: str, widget_key: str):
    current = st.session_state[ACCOUNT_SELECTED_ACCOUNT]

    copy = current.model_copy(
        update={field: st.session_state[widget_key]}
    )

    st.session_state[ACCOUNT_SELECTED_ACCOUNT] = copy
    db.save(copy, op="edit")


def account_details_grid(account: BankAccount):
    account = st.session_state[ACCOUNT_SELECTED_ACCOUNT]
    grid = st.grid(2, vertical_alignment="center")

    def name_in():
        grid.write("Name")
        key = f"name_{account.id}"

        grid.text_input(
            label="Name",
            label_visibility="collapsed",
            value=account.name,
            required=True,
            validate=(r"^.{3,}$", "Name must be at least 3 characters long."),
            key=key,
            on_change=update_account,
            args=("name", key),
        )

    def monthly_limit_in():
        grid.write("Monthly Budget")
        key = f"monthly_limit_{account.id}"

        grid.number_input(
            label="Monthly Limit",
            label_visibility="collapsed",
            value=float(account.monthly_limit),
            min_value=0.0,
            max_value=10_000_000.0,
            step=10.0,
            key=key,
            on_change=update_account,
            args=("monthly_limit", key),
        )

    def color_in():
        with grid.container(
                horizontal=True,
                vertical_alignment="center",
                gap="xsmall"
        ):
            st.write("Color")
            st.badge("", icon=account.icon, color=account.color)

        with grid.cell():
            key = f"color_{account.id}"
            color_options = get_args(BadgeColor)

            st.selectbox(
                "Color",
                options=color_options,
                format_func=lambda c: f"{color_emojis[c]} {c.capitalize()}",
                label_visibility="collapsed",
                index=color_options.index(account.color),
                key=key,
                on_change=update_account,
                args=("color", key),
            )

    def icon_in():
        with grid.container(
                horizontal=True,
                vertical_alignment="center",
                gap="xsmall"
        ):
            st.write("Icon")
            st.badge("", icon=account.icon, color=account.color)

        with grid.cell():
            key = f"icon_{account.id}"

            st.selectbox(
                "Icon",
                options=icon_options,
                label_visibility="collapsed",
                index=icon_options.index(account.icon),
                key=key,
                on_change=update_account,
                args=("icon", key),
            )

    def currency_in():
        grid.write("Currency")

        with grid.cell():
            key = f"currency_{account.id}"
            currencies = list(Currency)

            st.selectbox(
                "Currency",
                label_visibility="collapsed",
                options=currencies,
                index=currencies.index(account.currency),
                format_func=lambda c: f"{c.code} - {c.currency_name}",
                key=key,
                on_change=update_account,
                args=("currency", key),
            )

    name_in()
    monthly_limit_in()
    color_in()
    icon_in()
    currency_in()
