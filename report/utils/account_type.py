from enum import Enum


class AccountType(Enum):
    EXPENSE = 1,
    EXPENSE_AFTER_DEDUCTION = 2
    INCOME = 3
    ASSETS = 4
    LIABILITY = 5
