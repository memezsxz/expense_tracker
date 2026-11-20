import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.account_details_grid import account_details_grid
from app.components.stat_container import stat_container
from app.data.models import BankAccount
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import ACCOUNT_SELECTED_ACCOUNT, ACCOUNTS_ALERT_MSG, ACCOUNTS_ALERT_ICON
from app.db.database import db

selected = st.session_state.get(ACCOUNT_SELECTED_ACCOUNT)
account = BankAccount.model_validate(selected.model_dump())
# account = BankAccount.model_validate(db.BankAccounts.head(3).to_dict(orient="records")[2])
# st.session_state[ACCOUNT_SELECTED_ACCOUNT] = account

if not account:
    error_msg = "Could not reach account details"
    st.session_state[ACCOUNTS_ALERT_MSG] = f":red[{error_msg}]"
    st.session_state[ACCOUNTS_ALERT_ICON] = "🚨"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))


def delete_account(to_delete_account: BankAccount):
    account_id = str(to_delete_account.id)

    if (
            (db.Transactions["account_id"] == account_id) |
            (db.Transactions["to_account_id"] == account_id)
    ).any():
        st.session_state[ACCOUNTS_ALERT_MSG] = ":red[Cannot delete an account that has transactions.]"
        st.session_state[ACCOUNTS_ALERT_ICON] = "🚨"

        st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))
        return

    db.save(to_delete_account, "delete")

    st.session_state[ACCOUNTS_ALERT_MSG] = ":green[Account Deleted Successfully]"
    st.session_state[ACCOUNTS_ALERT_ICON] = "✅"

    st.switch_page(st.Page(PAGE_PATH.MANAGE_ACCOUNTS))


with st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
        gap="small",
):
    st.title(account.name, icon=account.icon, anchor=False)

    st.button(
        "",
        type="primary",
        icon=":material/delete:",
        on_click=lambda: delete_account(account),
    )
    # TODO: add delete

st.divider()

account_details_grid(account)

st.divider()

st.markdown("### Stats:", anchors=False)
# TODO: add stats

col1, col2, col3 = st.columns(3)

df = db.Transactions[(db.Transactions["account_id"] == str(account.id)) & db.Transactions["to_account_id"].isna()]
# to_df = db.Transactions[(db.Transactions["to_account_id"] == str(account.id))]
df["date"] = pd.to_datetime(df["date"])


total_spend = df[(df["type"] == "expense")]["amount"].sum()
total_income = df[(df["type"] == "income")]["amount"].sum()

stat_container(col1, f"**Total Income**", f"{total_income:.2f}")
stat_container(col2, f"**Total Expense**", f"{total_spend:.2f}")

daily_spend_avg = (
        df[df["type"] == "expense"]["amount"].sum()
        / ((df["date"].max() - df["date"].min()).days + 1)
)

stat_container(col3, f"**Avg daily Spend**", f"{daily_spend_avg:.2f}")

# balance history

filtered_spend = (
    df[df["type"] == "expense"]
    .set_index("date")["amount"]
    .resample("ME").sum()
    .reset_index()
)

filtered_income = (
    df[df["type"] == "income"]
    .set_index("date")["amount"]
    .resample("ME").sum()
    .reset_index()
)

filtered_spend["type"] = "Expense"
filtered_income["type"] = "Income"
combined = pd.concat([filtered_spend, filtered_income])

fig = px.line(
    combined,
    x="date",
    y="amount",
    color="type",
    markers=True,
    color_discrete_map={
        "Expense": "red",
        "Income": "green",
    },
    title="Monthly Income vs Expenses",
    labels={
        "date": "Month",
        "amount": "Amount",
        "type": "Transaction Type",
    },
)

with st.container(border=True, horizontal_alignment="center"):
    st.plotly_chart(fig, key="asd")

expenses = db.Transactions[
    db.Transactions["type"] == "expense"
    ]

totals = (
    expenses.groupby("category_id")["amount"]
    .sum()
    .reset_index()
)

totals = totals.merge(
    db.Categories,
    left_on="category_id",
    right_on="id"
)

fig = px.pie(
    totals,
    names="name",
    values="amount",
    hole=0.5,
    title="Spending by Category",
)

with st.container(border=True, horizontal_alignment="center"):
    st.plotly_chart(fig)

df = (db.Transactions[(db.Transactions["account_id"] == str(account.id))]
      .merge(
    db.Categories,
    left_on="category_id",
    right_on="id"
).drop(columns=["id_x",
                "account_id",
                "category_id",
                "id_y",
                "color",
                "icon",
                "date_created"]
       )
      .rename(columns={"name": "category"})
      )

st.divider()
st.dataframe(df, hide_index=True)
