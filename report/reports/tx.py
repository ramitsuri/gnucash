from decimal import Decimal
from utils.date import get_current_year, get_current_month, get_previous_month
from utils import json_ut


class Transaction:
    def __init__(self, date, total, splits, description, num):
        self.date = date
        self.total = total
        self.splits = splits
        self.description = description
        self.num = num


class Split:
    def __init__(self, amount, account):
        self.amount = amount
        self.account = account


def print_transactions(transactions, account_names, years, time_delta, config, json_path):
    if config['current_and_last_month_only']:
        years = [get_current_year(time_delta)]
        months = [get_previous_month(time_delta), get_current_month(time_delta)]
    else:
        months = [*range(1, 13)]

    for year in years:
        path = json_path + "transactions/" + str(year) + '/'
        for month in months:
            transactions_for_month = __print_transactions(transactions, account_names, year, month)
            file_name = str(month).zfill(2)
            json_ut.print_transactions(path, file_name, transactions_for_month)


def __print_transactions(transactions, account_names, year, month):
    result = []
    for transaction in transactions:
        if transaction.post_date.year != year:
            continue
        if transaction.post_date.month != month:
            continue

        splits = []
        total = Decimal("0.0")
        for split in transaction.splits:
            if split.is_debit:
                total += split.value
                splits.append(Split(split.value, __get_account_name(split.account, account_names)))
            else:
                splits.append(Split(split.value, __get_account_name(split.account, account_names)))

        result.append(Transaction(transaction.post_date, total, splits, transaction.description, transaction.num))

    return result


def __get_account_name(account, account_names):
    if not account.fullname:
        return account_names[account.guid]
    else:
        return account.fullname
