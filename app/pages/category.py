import streamlit as st

from app.components.category_details_grid import category_details_grid
from app.data.models import Category
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import CATEGORY_SELECTED_CATEGORY, CATEGORIES_ALERT_ICON, CATEGORIES_ALERT_MSG
from app.db.database import db

category = Category.model_validate(st.session_state.get(CATEGORY_SELECTED_CATEGORY))

if not category:
    error_msg = "Could not reach category details"
    st.session_state[CATEGORIES_ALERT_MSG] = f":red[{error_msg}]"
    st.session_state[CATEGORIES_ALERT_ICON] = "🚨"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_CATEGORIES))


def delete_account(to_delete_category: Category):
    db.save(to_delete_category, "delete")
    success_msg = "Account Deleted Successfully"
    st.session_state[CATEGORIES_ALERT_MSG] = f":green[{success_msg}]"
    st.session_state[CATEGORIES_ALERT_ICON] = "✅"

    st.switch_page(st.Page(PAGE_PATH.MANAGE_CATEGORIES))


with st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
        gap="small",
):
    st.title(category.name, icon=category.icon, anchor=False)

    st.button(
        "",
        type="primary",
        icon=":material/delete:",
        on_click=delete_account,
        args=(category,),
    )

st.divider()

category_details_grid(category)

st.divider()

st.markdown("### Stats:", anchors=False)
# TODO: add stats
