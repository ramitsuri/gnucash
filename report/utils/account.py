from utils.date import get_start_date, get_end_date
from decimal import Decimal

_ROOT = "ROOT"


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


def get_totals_for_accounts(accounts, account_type, year, time_delta):
    account_infos = __get_relevant_accounts(accounts, account_type)
    __set_monthly_balances_on_accounts(account_infos, year, time_delta)
    account_totals = __convert_to_account_totals(account_infos)
    return account_totals


def get_totals_for_each_month(account_totals):
    month_total = AccountTotal("Total", "Total")
    for account_total in account_totals:
        month_index = 0
        for account_balance in account_total.balances:
            existing_amount = month_total.balances[month_index].amount
            month_total.balances[month_index].amount = existing_amount + account_balance.amount
            month_index += 1
        month_total.total = month_total.total + account_total.total
    return month_total


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


def __convert_to_account_totals(account_infos):
    totals = []
    for info in account_infos:
        total = AccountTotal(info.account.name, info.account.fullname)
        for balance_info in info.balance_infos:
            total.balances[balance_info.month - 1].amount = balance_info.amount
            total.total += balance_info.amount

        if info.children:
            for child in info.children:
                child_total = AccountTotal(child.account.name, child.account.fullname)
                for child_balance_info in child.balance_infos:
                    child_total.balances[child_balance_info.month - 1].amount = child_balance_info.amount
                    child_total.total += child_balance_info.amount
                total.children.append(child_total)
        totals.append(total)
    return totals


# Build a list of accounts filtered according to the account_type
def __get_relevant_accounts(accounts, account_type):
    account_infos = []
    completed_children = set()
    for account in accounts:
        if account.parent.type == _ROOT:
            continue
        if account.type != account_type:
            continue
        if account in completed_children:
            continue

        if not account.children:  # children empty
            account_infos.append(_AccountInfo(account))
        else:
            account_info = _AccountInfo(account)
            for child in account.children:
                completed_children.add(child)
                account_info.children.append(_AccountInfo(child))
            account_infos.append(account_info)

    return account_infos


# Calculates and sets monthly balances on accounts
def __set_monthly_balances_on_accounts(account_infos, year, time_delta):
    for info in account_infos:
        if not info.children:  # children empty
            info.balance_infos = __get_balances_for_account_for_year(info.account, year, time_delta)
        else:
            for child in info.children:
                child.balance_infos = __get_balances_for_account_for_year(child.account, year, time_delta)
            info.balance_infos = __calculate_and_get_balances_for_parent(info)


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
