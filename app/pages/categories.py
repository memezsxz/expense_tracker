import streamlit as st

from app.data.mock_data import  mock_categories
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNTS_ERROR, ACCOUNT_SELECTED_ACCOUNT, CATEGORIES_ERROR, \
    CATEGORY_SELECTED_CATEGORY

# TODO: add retrival
categories = mock_categories

st.title('Manage Categories')

st.space(size="small")

for category in categories:
    cat_con = st.container(border=True)
    with cat_con:  # click on to view Account page
        col1, col2, col3 = st.columns([0.8, 9, 0.5], vertical_alignment="center")

        with col1:
            # account icon in circle of color
            st.badge(label="", icon=category.icon, color=category.color)

        with col2:
            # account name
            st.write(category.name)

        with col3:
            if st.button("", type="tertiary", icon=":material/manage_search:"):
                st.session_state[CATEGORY_SELECTED_CATEGORY] = category
                st.switch_page(st.Page(PAGE_PATH.CATEGORY))

error_msg = st.session_state.get(CATEGORIES_ERROR)
if error_msg:
    st.toast(f":red[{error_msg}]", icon="🚨")
    st.session_state[CATEGORIES_ERROR] = None
