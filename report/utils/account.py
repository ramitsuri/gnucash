from utils.date import get_start_date, get_end_date
from decimal import Decimal


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


class _AccountInfo:
    def __init__(self, account):
        self.account = account
        self.children = []  # List of _AccountInfo
        self.balance_infos = []  # List of _BalanceInfo


class _BalanceInfo:
    def __init__(self, month, amount):
        self.month = month  # Month number ranging from 1-12 (inclusive)
        self.amount = amount  # Decimal amounts


def get_totals_for_accounts(root_account, year, time_delta, with_running_balance=False):
    root_account_info = __get_relevant_accounts(root_account)
    if with_running_balance:
        __set_monthly_running_balances_on_accounts(root_account_info, year, time_delta)
    else:
        __set_monthly_balances_on_accounts(root_account_info, year, time_delta)
    account_total = __convert_to_account_totals(root_account_info)
    return account_total


# TODO convert to use the tree root account
def filter_out_and_get_totals(account_totals, exclude_parents, exclude_children):
    totals = []
    for account_total in account_totals:
        if any(exclude_parent in account_total.fullname for exclude_parent in exclude_parents):
            continue

        if not account_total.children:  # children empty
            totals.append(account_total)
        else:
            new_account_total = AccountTotal(account_total.name, account_total.fullname)
            for child_total in account_total.children:
                if any(exclude_child in child_total.fullname for exclude_child in exclude_children):
                    continue
                new_account_total.children.append(child_total)
                new_account_total.total += child_total.total
                for child_total_balance in child_total.balances:
                    new_account_total.balances[child_total_balance.month - 1].amount += child_total_balance.amount

            totals.append(new_account_total)

    return totals


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
