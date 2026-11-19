from iso4217 import Currency

from app.data.models import BankAccount, Category

bank_accounts = [
    BankAccount(
        name="NBB",
        balance=20,
        color="red",
        icon=":material/savings:",
        currency=Currency.BHD,
    )
]

mock_categories = [
    Category(
        name="Transport",
        color="red",
        icon=":material/savings:",
    )
]
