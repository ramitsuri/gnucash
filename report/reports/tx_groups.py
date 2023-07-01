from decimal import Decimal
from utils import json_ut


class TransactionGroup:
    def __init__(self, name, total):
        self.name = name
        self.total = total


def print_transaction_groups(transactions, config, json_path):
    transaction_groups = {}

    for group_config in config:
        identifier = group_config['identifier']
        transactions_for_identifier = [transaction for transaction in transactions if
                                       identifier == transaction.num]
        total = Decimal("0.0")
        for transaction_for_identifier in transactions_for_identifier:
            total += __get_transaction_amount(transaction_for_identifier)

        transaction_groups[identifier] = TransactionGroup(name=group_config['display_name'], total=total)

    path = json_path
    file_name = "TransactionGroups"
    json_ut.print_transaction_groups(path, file_name, list(transaction_groups.values()))


def __get_transaction_amount(transaction):
    amount = Decimal("0.0")
    for split in transaction.splits:
        if split.is_debit:
            amount += split.value
    return amount

