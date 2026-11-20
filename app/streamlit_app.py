import streamlit as st

# initiate db
import db.database as db  # noqa: F401
from app.data.page_paths import PAGE_PATH

pages = {
    "": [
        st.Page(
            PAGE_PATH.HOME,
            title="Home",
            # icon="🔥",
            # help="test",
            default=True
        ),
        st.Page(PAGE_PATH.STATS, title="Stats")
    ],
    "Settings": [
        st.Page(PAGE_PATH.MANAGE_CATEGORIES, title="Manage Categories"),
        st.Page(PAGE_PATH.MANAGE_ACCOUNTS, title="Manage Accounts"),
        st.Page(PAGE_PATH.ACCOUNT, visibility="hidden"),
        st.Page(PAGE_PATH.CATEGORY, visibility="hidden")
    ],

}

pg = st.navigation(pages)
pg.run()
