import os
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

class Database:
    _categories_path = DATA_DIR / "categories.csv"
    _transactions_path = DATA_DIR / "transactions.csv"
    _bank_accounts_path = DATA_DIR / "bank_accounts.csv"
    _attachments_path = DATA_DIR / "attachments.csv"

    def __init__(self):
        self.BankAccount: pd.DataFrame = (
            pd.read_csv(self._bank_accounts_path)
            if os.path.isfile(self._bank_accounts_path)
            else pd.DataFrame()
        )

        self.Categories: pd.DataFrame = (
            pd.read_csv(self._categories_path)
            if os.path.isfile(self._categories_path)
            else pd.DataFrame()
        )

        self.Transactions: pd.DataFrame = (
            pd.read_csv(self._transactions_path)
            if os.path.isfile(self._transactions_path)
            else pd.DataFrame()
        )

        self.Attachments: pd.DataFrame = (
            pd.read_csv(self._attachments_path)
            if os.path.isfile(self._attachments_path)
            else pd.DataFrame()
        )

    def save_df(self, df: pd.DataFrame):
        if df is self.BankAccount:
            path = self._bank_accounts_path
        elif df is self.Categories:
            path = self._categories_path
        elif df is self.Transactions:
            path = self._transactions_path
        elif df is self.Attachments:
            path = self._attachments_path
        else:
            raise ValueError("Unknown DataFrame")

        df.to_csv(path, index=False)

db = Database()
