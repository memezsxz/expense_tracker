from enum import Enum
from pathlib import Path


class PAGE_PATH(Path, Enum):
    HOME = Path("pages/home.py")
    STATS = Path("pages/stats.py")
    MANAGE_ACCOUNTS = Path("pages/accounts.py")
    ACCOUNT = Path("pages/account.py")
    MANAGE_CATEGORIES = Path("pages/categories.py")
    CATEGORY = Path("pages/category.py")
