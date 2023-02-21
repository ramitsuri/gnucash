from utils.date import get_start_date, get_end_date
from decimal import Decimal
from enum import Enum


class AccountTotal:
    def __init__(self, name, fullname):
        self.name = name  # Account name
        self.fullname = fullname  # Account full name
        self.children = []  # List of AccountTotal
        self.balances = []  # List of Balance
        for month in range(1, 13):  # 1-12 for months, range end is not included
            self.balances.append(Balance(month, Decimal("0.0")))
        self.total = Decimal("0.0")


class Balance:
    def __init__(self, month, amount):
        self.month = month  # Month number ranging from 1-12 (inclusive)
        self.amount = amount  # Decimal amounts


class FilterType(Enum):
    INCLUDE = 1
    EXCLUDE = 2


class _AccountInfo:
    def __init__(self, account):
        self.account = account
        self.children = []  # List of _AccountInfo
        self.balance_infos = []  # List of _BalanceInfo


class _BalanceInfo:
    def __init__(self, month, amount):
        self.month = month  # Month number ranging from 1-12 (inclusive)
        self.amount = amount  # Decimal amounts


def get_totals_for_accounts(root_account, year, time_delta, filter_accounts, filter_type, with_running_balance=False):
    if not filter_accounts:
        root_account_info = __get_relevant_accounts(root_account)
    else:
        root_account_info = __get_relevant_accounts_with_filter(root_account, filter_accounts, filter_type)
    if with_running_balance:
        __set_monthly_running_balances_on_accounts(root_account_info, year, time_delta)
    else:
        __set_monthly_balances_on_accounts(root_account_info, year, time_delta)
    account_total = __convert_to_account_totals(root_account_info)
    return account_total


def set_balances_on_parents(root_account_total):
    for child_account_total in root_account_total.children:
        set_balances_on_parents(child_account_total)
    if not root_account_total.children:
        return
    balances = []
    months = range(1, 13)
    total = Decimal("0.0")
    for month in months:
        month_amount = Decimal("0.0")
        for child_account_total in root_account_total.children:
            balance = child_account_total.balances[month - 1]
            month_amount += balance.amount
            total += balance.amount
        balances.append(Balance(month, month_amount))
    root_account_total.balances = balances
    root_account_total.total = total


def __convert_to_account_totals(root_account_info):
    children = [__convert_to_account_totals(child) for child in root_account_info.children]
    total = AccountTotal(root_account_info.account.name, root_account_info.account.fullname)
    total.children = children
    for balance_info in root_account_info.balance_infos:
        total.balances[balance_info.month - 1].amount = balance_info.amount
        total.total += balance_info.amount
    return total


# Build _AccountInfo tree that holds PieCash Accounts.
def __get_relevant_accounts(root_account):
    children = [__get_relevant_accounts(child) for child in root_account.children]
    account_info = _AccountInfo(root_account)
    account_info.children = children
    return account_info


# Build _AccountInfo tree that holds PieCash Accounts.
def __get_relevant_accounts_with_filter(root_account, filter_accounts, filter_type):
    # A leaf account should definitely be able to be included as a child
    if not root_account.children and not __can_include_account(root_account, filter_accounts, filter_type):
        return None
    children = [__get_relevant_accounts_with_filter(child, filter_accounts, filter_type) for child in
                root_account.children]
    children_not_none = [child for child in children if child is not None]
    if not children_not_none and root_account.children:
        return None
    account_info = _AccountInfo(root_account)
    account_info.children = children_not_none
    return account_info


def __can_include_account(account, filter_accounts, filter_type):
    if not filter_accounts:  # Include account if no filter_accounts provided
        return True

    if filter_type == FilterType.INCLUDE:
        return account.fullname in filter_accounts
    else:
        return account.fullname not in filter_accounts


# Traverses the tree in post order and sets balances. If account has no children, balances are evaluated, if there are
# children, balances are calculated from children
def __set_monthly_balances_on_accounts(root_account_info, year, time_delta):
    for account_info in root_account_info.children:
        __set_monthly_balances_on_accounts(account_info, year, time_delta)
    if root_account_info.children:
        root_account_info.balance_infos = __calculate_and_get_balances_for_parent(root_account_info)
    else:
        root_account_info.balance_infos = __get_balances_for_account_for_year(root_account_info.account, year,
                                                                              time_delta)


# Traverses the tree in post order and sets balances. If account has no children, balances are evaluated, if there are
# children, balances are calculated from children
def __set_monthly_running_balances_on_accounts(root_account_info, year, time_delta):
    for account_info in root_account_info.children:
        __set_monthly_running_balances_on_accounts(account_info, year, time_delta)
    root_account_info.balance_infos = __calculate_and_get_running_balances(root_account_info, year, time_delta)


# Calculates balances for all months for an account for a year
def __get_balances_for_account_for_year(account, year, time_delta):
    balance_infos = []
    months = range(1, 13)
    for month in months:
        balance_infos.append(_BalanceInfo(month, __get_amount_for_account_for_month(account, year, month, time_delta)))
    return balance_infos


# Calculates balances for an account for a year and month
def __get_amount_for_account_for_month(account, year, month, time_delta):
    start_date = get_start_date(year, month, time_delta)
    end_date = get_end_date(year, month, time_delta)
    amount = Decimal("0.0")
    for acc_split in account.splits:
        if start_date <= acc_split.transaction.post_date <= end_date:
            for split in acc_split.transaction.splits:
                if split.account.name == account.name:
                    amount += split.value
    return amount


# Calculates balances for parent from its child accounts
def __calculate_and_get_balances_for_parent(parent_account_info):
    balance_infos = []
    months = range(1, 13)
    for month in months:
        child_sum = Decimal("0.0")
        for child in parent_account_info.children:
            child_sum += child.balance_infos[month - 1].amount
        balance_infos.append(_BalanceInfo(month, child_sum))
    return balance_infos


# Calculates balances for parent from its child accounts
def __calculate_and_get_running_balances(account_info, year, time_delta):
    balance_infos = []
    months = range(1, 13)
    for month in months:
        end_of_month_date = get_end_date(year, month, time_delta)
        end_of_month_balance = account_info.account.get_balance(at_date=end_of_month_date)
        balance_infos.append(_BalanceInfo(month, end_of_month_balance))
    return balance_infos
