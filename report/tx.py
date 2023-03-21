from decimal import Decimal
from utils.date import get_current_year, get_current_month, get_previous_month
import utils.json_ut


class Transaction:
    def __init__(self, date, amount, from_accounts, to_accounts, description):
        self.date = date
        self.amount = amount
        self.from_accounts = from_accounts
        self.to_accounts = to_accounts
        self.description = description


def print_transactions(transactions, years, time_delta, config, json_path):
    if config['current_and_last_month_only']:
        years = [get_current_year(time_delta)]
        months = [get_previous_month(time_delta), get_current_month(time_delta)]
    else:
        months = [*range(1, 13)]

    for year in years:
        path = json_path + config['path'] + str(year) + '/'
        for month in months:
            transactions_for_month = __print_transactions(transactions, year, month)
            file_name = str(month).zfill(2)
            utils.json_ut.print_transactions(path, file_name, transactions_for_month)


def __print_transactions(transactions, year, month):
    result = []
    for transaction in transactions:
        if transaction.post_date.year != year:
            continue
        if transaction.post_date.month != month:
            continue

        to_accounts = []
        from_accounts = []
        amount = Decimal("0.0")
        for split in transaction.splits:
            if split.is_debit:
                amount += split.value
                to_accounts.append(split.account.fullname)
            else:
                from_accounts.append(split.account.fullname)

        result.append(Transaction(transaction.post_date, amount, from_accounts, to_accounts, transaction.description))

    return result
