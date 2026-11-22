import plotly.express as px
import streamlit as st

from app.components.show_missing import show_missing_and_stop
from app.components.stat_container import stat_container
from app.db.database import db
from app.utils.stats_util import get_transactions_merge_account, get_top_stats, get_monthly_trends, get_category_totals

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

df = get_transactions_merge_account(currency)

if df.empty:
    show_missing_and_stop("Add transactions to see your statistics for this currency!")

st.subheader("Overview", divider="gray", anchor=False)

(
    expenses,
    income,
    total_expenses,
    total_income,
    daily_spend_avg,
    net_cash_flow,
    savings_rate
) = get_top_stats(df)

st.subheader("Top Transactions", divider="gray", anchor=False)

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

monthly_trends = get_monthly_trends(expenses, income)
fig = px.bar(
    monthly_trends,
    x="date",
    y="amount",
    color="type",
    barmode="group",
    color_discrete_map={
        "Expense": "red",
        "Income": "green",
    },
    title="Monthly Income vs Expenses",
    labels={ # assisted by CHAT-GPT
        "date": "Month",
        "amount": "Amount",
        "type": "Transaction Type",
    },
)

with st.container(border=True):
    st.plotly_chart(fig, width="stretch")

category_totals = get_category_totals(expenses)
fig = px.pie(
    category_totals,
    names="name",
    values="amount",
    hole=0.4,
    title="Spending by Category",
)

fig.update_traces(textinfo="label+percent") # assisted by CHAT-GPT

with st.container(border=True):
    st.plotly_chart(fig, width="stretch")
