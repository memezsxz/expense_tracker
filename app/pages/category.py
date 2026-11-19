import streamlit as st

from app.data.models import Category
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import CATEGORY_SELECTED_CATEGORY, \
    CATEGORIES_ERROR

category : Category = st.session_state.get(CATEGORY_SELECTED_CATEGORY)

if not category:
    st.session_state[CATEGORIES_ERROR] = "Could not reach category details"
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
    )
    # TODO: add delete
