import os
from pathlib import Path
from typing import Literal
from uuid import UUID

import pandas as pd
from pydantic import BaseModel

from app.data.models import BankAccount, Category, Transaction, TransactionView, TransactionType

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

OPERATION = Literal[
    "add",
    "edit",
    "delete",
]

TABLES = {
    BankAccount: "BankAccounts",
    Category: "Categories",
    Transaction: "Transactions",
    # Attachment: "Attachments",
}


class Database:
    _categories_path = DATA_DIR / "categories.csv"
    _transactions_path = DATA_DIR / "transactions.csv"
    _bank_accounts_path = DATA_DIR / "bank_accounts.csv"
    # _attachments_path = DATA_DIR / "attachments.csv"

    def __init__(self):
        self.BankAccounts: pd.DataFrame = self._load_data(self._bank_accounts_path)
        self.Categories: pd.DataFrame = self._load_data(self._categories_path)
        self.Transactions: pd.DataFrame = self._load_data(self._transactions_path)
        # self.Attachments: pd.DataFrame = self._load_data(self._attachments_path)

    def _load_data(self, path: Path) -> pd.DataFrame:
        return (pd.read_csv(path)
                if os.path.isfile(path)
                else pd.DataFrame()
                )

    def _save_df(self, df: pd.DataFrame):
        if df is self.BankAccounts:
            path = self._bank_accounts_path
        elif df is self.Categories:
            path = self._categories_path
        elif df is self.Transactions:
            path = self._transactions_path
        # elif df is self.Attachments:
        #     path = self._attachments_path
        else:
            raise ValueError("Unknown DataFrame")

        df.to_csv(path, index=False)

    def save(self, model: BaseModel, op: OPERATION):
        table_name = TABLES[type(model)]

        df = getattr(db, table_name).copy()
        model_dump = model.model_dump(mode="json")

        match op:
            case "add":
                df = pd.concat(
                    [df, pd.DataFrame([model_dump])],
                    ignore_index=True
                )

            case "edit":
                filtered = df["id"] == str(model_dump.get("id"))

                for field, value in model_dump.items():
                    df.loc[filtered, field] = value

            case "delete":
                df = df[df["id"] != str(model_dump.get("id"))].copy()

        setattr(db, table_name, df)
        db._save_df(df)

    def get_transactions_by_account_and_month(
            self,
            account_id: UUID,
            year: int,
            month: int
    ) -> list[TransactionView]:
        df = db.Transactions

        if df.empty:
            return []

        df = db.Transactions.copy()

        df["date"] = pd.to_datetime(df["date"])

        filtered = df[
            (
                    (df["account_id"] == str(account_id))
                    | (
                            (df["type"] == TransactionType.TRANSFER.value)
                            & (df["to_account_id"] == str(account_id))
                    )
            )
            & (df["date"].dt.year == year)
            & (df["date"].dt.month == month)
            ].sort_values("date", ascending=False)

        categories = {
            c.id: c
            for c in [
                Category.model_validate(row)
                for row in self.Categories.to_dict(orient="records")
            ]
        }

        accounts = {
            a.id: a
            for a in [
                BankAccount.model_validate(row)
                for row in self.BankAccounts.to_dict(orient="records")
            ]
        }

        return [
            TransactionView(
                transaction=t,
                category=categories.get(t.category_id),
                account=accounts.get(t.account_id),
            )
            for row in filtered.to_dict(orient="records")
            for t in [Transaction.model_validate(row)]
        ]


db = Database()
