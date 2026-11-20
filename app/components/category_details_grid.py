from typing import get_args

import streamlit as st

from app.data.colors import BadgeColor, color_emojis
from app.data.icons import icon_options
from app.data.models import Category
from app.data.streamlit_state_keys import CATEGORY_SELECTED_CATEGORY
from app.db.database import db


def update_category(field: str, widget_key: str):
    current = st.session_state[CATEGORY_SELECTED_CATEGORY]
    copy = current.model_copy(
        update={field: st.session_state[widget_key]}
    )

    st.session_state[CATEGORY_SELECTED_CATEGORY] = copy
    db.save(copy, op="edit")


def category_details_grid(category: Category):
    category = st.session_state[CATEGORY_SELECTED_CATEGORY]
    grid = st.grid(2, vertical_alignment="center")

    def name_in():
        grid.write("Name")
        key = f"name_{category.id}"

        grid.text_input(
            label="Name",
            label_visibility="collapsed",
            value=category.name,
            key=key,
            on_change=update_category,
            args=("name", key),
        )

    def color_in():
        with grid.container(
                horizontal=True,
                vertical_alignment="center",
                gap="xsmall"
        ):
            st.write("Color")
            st.badge("", icon=category.icon, color=category.color)

        with grid.cell():
            key = f"color_{category.id}"
            color_options = get_args(BadgeColor)

            st.selectbox(
                label="Color",
                options=color_options,
                format_func=lambda c: f"{color_emojis[c]} {c.capitalize()}",
                label_visibility="collapsed",
                index=color_options.index(category.color),
                key=key,
                on_change=update_category,
                args=("color", key),
            )

    def icon_in():
        with grid.container(
                horizontal=True,
                vertical_alignment="center",
                gap="xsmall"
        ):
            st.write("Icon")
            st.badge("", icon=category.icon, color=category.color)

        with grid.cell():
            key = f"icon_{category.id}"

            st.selectbox(
                "Icon",
                options=icon_options,
                label_visibility="collapsed",
                index=icon_options.index(category.icon),
                key=key,
                on_change=update_category,
                args=("icon", key),
            )

    name_in()
    color_in()
    icon_in()
