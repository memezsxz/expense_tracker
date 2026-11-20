from datetime import date

from iso4217 import Currency

from app.data.models import BankAccount
from app.data.models import Category, Transaction, TransactionType

mock_bank_accounts = [
    BankAccount(
        name="NBB",
        balance=20,
        color="red",
        icon=":material/savings:",
        currency=Currency.BHD,
    ),
    BankAccount(
        name="Al Salam",
        balance=20,
        color="violet",
        icon=":material/currency_exchange:",
        currency=Currency.BHD,
    )

]

mock_categories: list[Category] = [
    Category(
        name="Income",
        color="green",
        icon=":material/payments:",
    ),
    Category(
        name="Daily Expenses",
        color="blue",
        icon=":material/shopping_cart:",
    ),
    Category(
        name="Shopping & Entertainment",
        color="violet",
        icon=":material/shopping_bag:",
    ),
]

income, daily, shopping = mock_categories

account = mock_bank_accounts[0]

mock_transactions: list[Transaction] = [
    # October 5
    Transaction(
        title="Monthly Salary",
        amount=650.000,
        date=date(2026, 10, 5),
        type=TransactionType.INCOME,
        category_id=income.id,
        account_id=account.id
    ),
    Transaction(
        title="Grocery Shopping",
        amount=32.450,
        date=date(2026, 10, 5),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),

    # October 16
    Transaction(
        title="Fuel",
        amount=12.000,
        date=date(2026, 10, 16),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),
    Transaction(
        title="Restaurant Dinner",
        amount=18.750,
        date=date(2026, 10, 16),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),

    # October 27
    Transaction(
        title="Netflix Subscription",
        amount=5.500,
        date=date(2026, 10, 27),
        type=TransactionType.EXPENSE,
        category_id=shopping.id,
        account_id=account.id
    ),
    Transaction(
        title="Clothing Shopping",
        amount=45.900,
        date=date(2026, 10, 27),
        type=TransactionType.EXPENSE,
        category_id=shopping.id,
        account_id=account.id
    ),

    # November 3
    Transaction(
        title="Monthly Salary",
        amount=650.000,
        date=date(2026, 11, 3),
        type=TransactionType.INCOME,
        category_id=income.id,
        account_id=account.id
    ),
    Transaction(
        title="Supermarket",
        amount=28.600,
        date=date(2026, 11, 3),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),

    # November 10
    Transaction(
        title="Car Fuel",
        amount=10.000,
        date=date(2026, 11, 10),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),
    Transaction(
        title="Coffee",
        amount=3.200,
        date=date(2026, 11, 10),
        type=TransactionType.EXPENSE,
        category_id=daily.id,
        account_id=account.id
    ),

    # November 18
    Transaction(
        title="Freelance Payment",
        amount=120.000,
        date=date(2026, 11, 18),
        type=TransactionType.INCOME,
        category_id=income.id,
        account_id=account.id
    ),
    Transaction(
        title="Electronics",
        amount=75.500,
        date=date(2026, 11, 18),
        type=TransactionType.EXPENSE,
        category_id=shopping.id,
        account_id=account.id
    ),
]
