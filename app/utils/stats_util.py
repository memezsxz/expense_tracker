import pandas as pd

from app.db.database import db


def get_transactions_merge_account(selected_currency) -> pd.DataFrame:
    df = db.Transactions.merge(
        db.BankAccounts[["id", "currency"]],
        left_on="account_id",
        right_on="id",
    )
    df["date"] = pd.to_datetime(df["date"])

    df = df[df["currency"] == selected_currency]

    return df


def get_top_stats(df: pd.DataFrame):
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

    return (
        expenses,
        income,
        total_expenses,
        total_income,
        daily_spend_avg,
        net_cash_flow,
        savings_rate
    )


def get_monthly_trends(expenses: pd.DataFrame, income: pd.DataFrame):
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

    return combined


def get_category_totals(expenses):
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

    return category_totals
