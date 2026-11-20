import pandas as pd
import plotly.express as px
import streamlit as st

from app.components.category_details_grid import category_details_grid
from app.components.stat_container import stat_container
from app.data.models import Category
from app.data.page_paths import PAGE_PATH
from app.data.streamlit_state_keys import CATEGORY_SELECTED_CATEGORY, CATEGORIES_ALERT_ICON, CATEGORIES_ALERT_MSG
from app.db.database import db

selected = st.session_state.get(CATEGORY_SELECTED_CATEGORY)
category = Category.model_validate(selected.model_dump())

# category = Category.model_validate(db.Categories.head(1).to_dict(orient="records")[0])
# st.session_state[CATEGORY_SELECTED_CATEGORY] = category

if not category:
    error_msg = "Could not reach category details"
    st.session_state[CATEGORIES_ALERT_MSG] = f":red[{error_msg}]"
    st.session_state[CATEGORIES_ALERT_ICON] = "🚨"
    st.switch_page(st.Page(PAGE_PATH.MANAGE_CATEGORIES))


def delete_category(to_delete_category: Category):
    category_id = str(to_delete_category.id)

    if (db.Transactions["category_id"] == category_id).any():
        st.error("Cannot delete a category that has transactions.")
        return

    db.save(to_delete_category, "delete")

    st.session_state[CATEGORIES_ALERT_MSG] = ":green[Category Deleted Successfully]"
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
        on_click=delete_category,
        args=(category,),
    )

st.divider()

category_details_grid(category)

st.divider()

st.markdown("### Stats:", anchors=False)
# TODO: add stats

col1, col2, col3, col4 = st.columns(4, )

df = db.Transactions[db.Transactions["category_id"] == str(category.id)].reset_index()

# total spending in category

total_spend = df[(df["type"] == "expense")]["amount"].sum()
total_income = df[(df["type"] == "income")]["amount"].sum()

stat_container(col1, f"**Total spend**", f"{total_spend:.2f}")
stat_container(col2, f"**Total income**", f"{total_income:.2f}")

# number of transactions
total_transactions = df.shape[0]

stat_container(col3, f"**Total transactions**", f"{total_transactions}")

# percentage of overall expenses
overall = (db.Transactions[(db.Transactions["type"] == "expense")]
           .groupby("category_id")["amount"]
           .sum()
           .reset_index()
           )

overall["percentage"] = overall["amount"] / overall["amount"].sum() * 100
overall_percentage = overall[overall["category_id"] == str(category.id)]["percentage"].values[0]

stat_container(col4, f"**Overall Spending**", f"{overall_percentage:.2f}%")

# monthly spending line chart
df["date"] = pd.to_datetime(df["date"])

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
    st.plotly_chart(fig)

# history
df = df.drop(columns=["id", "category_id"])
st.divider()
st.dataframe(df, hide_index=True)
