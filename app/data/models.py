import datetime as dt
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, StringConstraints


class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

class TransactionType(str, Enum):
    INCOME = "income"
    TRANSFER = "transfer" # transfer between accounts
    EXPENSE = "expense"

# screen to add bank accounts
# allow select for a color
# allow select for an icon
# allow setting the current balance
# allow deleting an account
# don't allow duplicate account names

HexColor = Annotated[
    str,
    Field(pattern=r"^#[0-9a-fA-F]{6}$")
]

NonEmptyId = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=36)
]

class BankAccount(BaseModel):
    """
    The bank account
    """
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=3)
    balance: int = Field(ge=0, default=0)
    color: HexColor
    icon: str = Field()

# add edit and view delete
# view stats
# no duplicate
class Category(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=3)
    color: HexColor
    icon: str = Field()

# add edit view delete
class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=3, default="") # default should be the category name
    account_id: NonEmptyId
    category_id: NonEmptyId
    amount: int = Field(gt=0)
    date: dt.date = Field(default_factory=dt.date.today)
    type: TransactionType
