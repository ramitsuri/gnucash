import calendar
import json
from datetime import datetime, timezone, timedelta
from decimal import Decimal

import piecash
from piecash import Transaction, Split


def to_decimal(float_value):
    return Decimal(str(float_value))


def get_date(date):
    year = date['year']
    month = date['month']
    day = calendar.monthrange(year, month)[1]
    return datetime(year, month, day, 10, 0, 0, 0, timezone(timedelta(hours=4))).date()


def read_json():
    f = open('new_data.json')
    new_data = json.load(f)
    f.close()
    return new_data


def read_and_update_account_values(account_list, file):
    book = piecash.open_book(file, readonly=True, open_if_lock=True)

    for account in account_list:
        found_account = book.accounts(fullname=account['base_account'])
        account['new_value'] = to_decimal(account['new_value']) - to_decimal(found_account.get_balance())

    book.close()
    return account_list


def add_transactions(details, account_list, file):
    book = piecash.open_book(file, readonly=False, open_if_lock=True)

    transfer_account = book.accounts(fullname=details['transfer_account'])

    for account in account_list:
        other_account = book.accounts(fullname=account['transfer_account'])
        split1 = Split(account=transfer_account, value=account['new_value'] * -1)
        split2 = Split(account=other_account, value=account['new_value'])

        Transaction(
            post_date=get_date(details['date']),
            currency=book.default_currency,
            description=details['description'],
            splits=[
                split1,
                split2
            ]
        )

    book.save()
    book.close()


def main():
    new_values = read_json()
    gnu_file = new_values['details']['file']
    accounts = read_and_update_account_values(new_values['accounts'], gnu_file)
    add_transactions(new_values['details'], accounts, gnu_file)


if __name__ == "__main__":
    main()
