import datetime as dt
from enum import Enum
from uuid import UUID, uuid4

import pandas as pd
from iso4217 import Currency
from pydantic import BaseModel, Field, field_validator

from app.data.colors import BadgeColor


class TransactionType(str, Enum):
    INCOME = "income"
    TRANSFER = "transfer"  # transfer between accounts
    EXPENSE = "expense"


# screen to add bank accounts
# allow select for a color
# allow select for an icon
# allow setting the current balance
# allow deleting an account
# don't allow duplicate account names

class BankAccount(BaseModel):
    """
    The bank account
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=3)
    balance: int = Field(ge=0, default=0)
    color: BadgeColor = Field(default="blue")
    icon: str = Field()
    currency: Currency = Field(default=Currency.BHD)
    date_created: dt.date = Field(default_factory=dt.date.today)


# add edit and view delete
# view stats
# no duplicate
class Category(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=3)
    color: BadgeColor = Field(default="blue")
    icon: str = Field()
    date_created: dt.date = Field(default_factory=dt.date.today)


# add edit view delete
class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=3, default="Default")  # default should be the category name
    account_id: UUID = Field()
    to_account_id: UUID | None = None
    category_id: UUID | None = None
    amount: float = Field(gt=0)
    date: dt.date = Field(default_factory=dt.date.today)
    type: TransactionType
    notes: str = ""

    @field_validator("notes", mode="before")
    @classmethod
    def handle_empty_notes(cls, value):
        return "" if pd.isna(value) else value

    @field_validator("to_account_id", "category_id", mode="before")
    @classmethod
    def handle_empty_uuid(cls, value):
        if value is None or value == "" or pd.isna(value):
            return None

        return value

class TransactionView(BaseModel):
    transaction: Transaction
    category: Category | None = None
    account: BankAccount | None = None
