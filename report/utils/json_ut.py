import jsonpickle
from decimal import Decimal
from utils.date import current_utc
import os, os.path


def print_report(path, report_name, file_name, root_account_total):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    time = current_utc()
    report = _Report(report_name, time, root_account_total)
    json_string = jsonpickle.encode(report, unpicklable=False)
    with __safe_open(path + file_name + '.json') as file:
        file.writelines(json_string)


def print_transactions(path, file_name, transactions):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    time = current_utc()
    _transactions = _Transactions(time, transactions)
    json_string = jsonpickle.encode(_transactions, unpicklable=False)
    with __safe_open(path + file_name + '.json') as file:
        file.writelines(json_string)


def print_transaction_groups(path, file_name, transaction_groups):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    time = current_utc()
    _transaction_groups = _TransactionGroups(time, transaction_groups)
    json_string = jsonpickle.encode(_transaction_groups, unpicklable=False)
    with __safe_open(path + file_name + '.json') as file:
        file.writelines(json_string)


class _Report:
    def __init__(self, name, time, account_total):
        self.name = name
        self.time = time
        self.account_total = account_total


class _Transactions:
    def __init__(self, time, transactions):
        self.time = time
        self.transactions = transactions


class _TransactionGroups:
    def __init__(self, time, transaction_groups):
        self.time = time
        self.transaction_groups = transaction_groups


class _DecimalHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Decimal, data):
        return str(obj)


def __safe_open(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')
