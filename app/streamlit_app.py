import streamlit as st

# initiate db
import db.database as db  # noqa: F401
from app.data.page_paths import PAGE_PATH

pages = {
    "": [
        st.Page(
            PAGE_PATH.HOME,
            title="View All",
            # icon="🔥",
            # help="test",
            default=True
        ),
        st.Page(PAGE_PATH.STATS, title="Financial Dashboard"),
        st.Page(PAGE_PATH.MANAGE_CATEGORIES, title="Manage Categories"),
        st.Page(PAGE_PATH.MANAGE_ACCOUNTS, title="Manage Accounts"),
        st.Page(PAGE_PATH.ACCOUNT, visibility="hidden"),
        st.Page(PAGE_PATH.CATEGORY, visibility="hidden")

    ],
}

st.set_page_config(
    page_title="Income Exchange",
    layout="centered",
    page_icon="media/favicon.png",
    initial_sidebar_state="expanded",
)

st.html("""
<style>
.stAppHeader [data-testid="stTopNav"] {
    position: absolute !important;
    left: 50% !important;
    top: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: 70vw !important;
    justify-content: center !important;
}
</style>
""")

pg = st.navigation(pages, position="top")
pg.run()