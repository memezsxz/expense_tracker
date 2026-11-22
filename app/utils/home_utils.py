import datetime

import pandas as pd

from app.data.models import BankAccount
from app.db.database import db


def get_monthly_spending(selected_bank_account: BankAccount, selected_month: datetime.date):
    df = db.Transactions
    df["date"] = pd.to_datetime(df["date"])

    monthly_spending = df[
        (df["account_id"] == str(selected_bank_account.id)) &
        (df["type"] == "expense") &
        (df["date"].dt.year == selected_month.year) &
        (df["date"].dt.month == selected_month.month)
        ]["amount"].sum()
    return monthly_spending
