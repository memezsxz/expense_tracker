import streamlit as st

from app.components.alert import show_alert
from app.data.models import Category
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import CATEGORY_SELECTED_CATEGORY, CATEGORIES_ALERT_MSG, CATEGORIES_ALERT_ICON
from app.db.database import db


def view_category(to_account: Category):
    st.session_state[CATEGORY_SELECTED_CATEGORY] = to_account
    st.switch_page(st.Page(PAGE_PATH.CATEGORY))


def add_category():
    new_category = Category(
        name="Default",
        color="yellow",
        icon=":material/savings:",
    )

    db.save(new_category, op="add")

    view_category(new_category)


categories: list[Category] = [
    Category.model_validate(row)
    for row in db.Categories.to_dict(orient="records")
]

with st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
        gap="small",
):
    st.title("Manage Categories")

    st.button(
        "Add New Category",
        type="secondary",
        icon=":material/add:",
        on_click=add_category,
    )

st.space(size="small")

for category in categories:
    cat_con = st.container(border=True)
    with cat_con:  # click on to view category page
        col1, col2, col3 = st.columns([0.8, 9, 0.5], vertical_alignment="center")

        with col1:
            # category icon in circle of color
            st.badge(label="", icon=category.icon, color=category.color)

        with col2:
            # category name
            st.write(category.name)

        with col3:
            st.button("",
                      type="tertiary",
                      icon=":material/manage_search:",
                      key=f"view_btn_{category.id}",
                      on_click=view_category,
                      args=(category,),
                      )

show_alert(CATEGORIES_ALERT_MSG, CATEGORIES_ALERT_ICON)
