import datetime

import streamlit as st

from app.data.streamlit_state_keys import HOME_SELECTED_MONTH


def change_month(direction: int):
    current = st.session_state[HOME_SELECTED_MONTH]

    if direction == -1:
        new_month = current - datetime.timedelta(days=1)
    else:
        new_month = current.replace(day=28) + datetime.timedelta(days=4)

    st.session_state[HOME_SELECTED_MONTH] = new_month.replace(day=1)


def change_month_col() -> datetime.date:
    prev_col, month_col, next_col = st.columns(
        [1, 8, 1],
        vertical_alignment="center"
    )

    with prev_col:
        st.button(
            "",
            icon=":material/chevron_left:",
            help="Previous month",
            key="prev_month",
            on_click=change_month,
            args=(-1,),
            width="stretch",
        )

    with month_col:
        selected_month = st.session_state[HOME_SELECTED_MONTH]

        st.markdown(
            f"#### {selected_month:%B} {selected_month.year}",
            text_alignment="center",
            anchors=False
        )

    with next_col:
        st.button(
            "",
            icon=":material/chevron_right:",
            help="Next month",
            key="next_month",
            on_click=change_month,
            args=(1,),
            width="stretch",
        )

    return st.session_state[HOME_SELECTED_MONTH]
