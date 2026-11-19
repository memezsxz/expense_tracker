from pathlib import Path
import streamlit as st

pages = {
    "": [
        st.Page(
            Path("pages/home.py"),
            title="Home",
            # icon="🔥",
            # help="test",
        ),
        st.Page(Path("pages/stats.py"), title="Stats")
    ],
    "Settings": [
        st.Page(Path("pages/categories.py"), title="Manage Categories"),
        st.Page(Path("pages/accounts.py"), title="Manage Accounts"),
    ],
}

pg = st.navigation(pages)
pg.run()
