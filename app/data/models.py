import datetime as dt
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from iso4217 import Currency
from pydantic import BaseModel, Field, StringConstraints

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
    title: str = Field(min_length=3, default="")  # default should be the category name
    account_id: UUID = Field()
    category_id: UUID = Field()
    amount: float = Field(gt=0)
    date: dt.date = Field(default_factory=dt.date.today)
    type: TransactionType
    notes: str = Field(default="")
    attachments: list[Attachment] = Field(default=[])  # ids for images

class TransactionView(BaseModel):
    transaction: Transaction
    category: Category | None = None
    account: BankAccount | None = None

class Attachment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    path: str = Field(min_length=3)
