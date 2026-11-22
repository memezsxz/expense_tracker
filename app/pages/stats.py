import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.stat_container import stat_container
from app.db.database import db

st.title("Financial Dashboard")

if db.BankAccounts.empty or db.Transactions.empty:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[Add accounts and transactions to see your statistics!]",
                    text_alignment="center"
                    )
    st.stop()

currency = st.selectbox(
    "Currency",
    options=sorted(db.BankAccounts["currency"].dropna().unique()),
)

df = db.Transactions.merge(
    db.BankAccounts[["id", "currency"]],
    left_on="account_id",
    right_on="id",
)
df["date"] = pd.to_datetime(df["date"])

df = df[df["currency"] == currency]

if df.empty:
    with st.container(vertical_alignment="center"):
        st.space(size="large")
        st.markdown(":gray[Add transactions to see your statistics for this currency!]",
                    text_alignment="center"
                    )
    st.stop()

st.subheader("Overview", divider="gray", anchor=False)


expenses = df[df["type"] == "expense"]
income = df[df["type"] == "income"]

total_expenses = expenses["amount"].sum()
total_income = income["amount"].sum()
net_cash_flow = total_income - total_expenses

number_of_days = (df["date"].max() - df["date"].min()).days + 1
daily_spend_avg = total_expenses / number_of_days

savings_rate = (
    net_cash_flow / total_income * 100
    if total_income > 0 else None
)

grid = st.grid(6, min_column_width=70, wrap=False)

stat_container(grid.cell(column_span=3), "**Total Expenses**", f"{total_expenses:,.3f}")
stat_container(grid.cell(column_span=3), "**Total Income**", f"{total_income:,.3f}")

stat_container(grid.cell(column_span=2), "**Avg Daily Spend**", f"{daily_spend_avg:,.3f}")
stat_container(grid.cell(column_span=2), "**Net Cash Flow**", f"{net_cash_flow:,.3f}")
stat_container(
    grid.cell(column_span=2),
    "**Savings Rate**",
    f"{savings_rate:.1f}%" if savings_rate is not None else "N/A"
)

st.subheader("Monthly Trends", divider="gray", anchor=False)

monthly_expenses = (
    expenses.set_index("date")["amount"]
    .resample("ME").sum()
    .reset_index()
)

monthly_income = (
    income.set_index("date")["amount"]
    .resample("ME").sum()
    .reset_index()
)

monthly_expenses["type"] = "Expense"
monthly_income["type"] = "Income"

combined = pd.concat([monthly_expenses, monthly_income])


fig = px.bar(
    combined,
    x="date",
    y="amount",
    color="type",
    barmode="group",
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

with st.container(border=True):
    st.plotly_chart(fig, width="stretch")


category_totals = (
    expenses.groupby("category_id")["amount"]
    .sum()
    .reset_index()
)

category_totals = category_totals.merge(
    db.Categories,
    left_on="category_id",
    right_on="id"
)

fig = px.pie(
    category_totals,
    names="name",
    values="amount",
    hole=0.4,
    title="Spending by Category",
)

fig.update_traces(textinfo="label+percent")

with st.container(border=True):
    st.plotly_chart(fig, width="stretch")