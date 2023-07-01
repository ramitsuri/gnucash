import json
import piecash

from utils.date import to_time_delta
from reports import savings, general, networth, tx, tx_groups, miscellaneous
from utils.print_type import PrintType
from utils.account_type import AccountType


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def main():
    config = read_config()
    gnu_cash_file = config['file']
    time_delta = to_time_delta(config['time_delta_hours'])
    years = config['years']
    print_types = list(map(lambda x: PrintType(x), config['print_types']))

    json_path = "output/json/"
    html_path = "output/html/"

    book = piecash.open_book(gnu_cash_file, readonly=True, open_if_lock=True)

    account_names = {}
    for account in book.accounts:
        account_names[account.guid] = account.fullname

    # Expense reports
    expense_config = config['expense']
    expense_root_account = book.root_account.children(name=expense_config['root_account_name'])
    expense = general.print_reports(AccountType.EXPENSE, print_types, expense_root_account, expense_config, time_delta,
                                    years, json_path, html_path)

    # Expense after deduction reports
    expense_after_deduction_config = config['expense_after_deduction']
    expense_after_deduction_root_account = book.root_account.children(
        name=expense_after_deduction_config['root_account_name'])
    expense_after_deduction = general.print_reports(AccountType.EXPENSE_AFTER_DEDUCTION, print_types,
                                                    expense_after_deduction_root_account,
                                                    expense_after_deduction_config, time_delta, years, json_path,
                                                    html_path)

    # Income reports
    income_config = config['income']
    income_root_account = book.root_account.children(name=income_config['root_account_name'])
    income = general.print_reports(AccountType.INCOME, print_types, income_root_account, income_config, time_delta,
                                   years, json_path, html_path)

    # Assets reports
    assets_config = config['assets']
    assets_root_account = book.root_account.children(name=assets_config['root_account_name'])
    assets = general.print_reports(AccountType.ASSETS, print_types, assets_root_account, assets_config, time_delta,
                                   years, json_path, html_path)

    # Liabilities reports
    liabilities_config = config['liabilities']
    liabilities_root_account = book.root_account.children(name=liabilities_config['root_account_name'])
    liabilities = general.print_reports(AccountType.LIABILITY, print_types, liabilities_root_account,
                                        liabilities_config, time_delta, years, json_path, html_path)

    # Networth reports
    networth_config = config['networth']
    networth.print_reports(print_types, liabilities, assets, networth_config, years, json_path, html_path)

    # Savings reports
    savings_config = config['savings']
    assets_root_account = book.root_account.children(name=savings_config['root_account_name'])
    saving = savings.print_reports(print_types, assets_root_account, savings_config, time_delta, years, json_path, html_path)

    # Transactions
    tx_config = config['transactions']
    tx.print_transactions(book.transactions, account_names, years, time_delta, tx_config, json_path)

    # Transaction Groups
    tx_groups_config = config['transaction_groups']
    tx_groups.print_transaction_groups(book.transactions, tx_groups_config, json_path)

    # Miscellaneous report
    miscellaneous_config = config['miscellaneous_report']
    miscellaneous.print_reports(miscellaneous_config, time_delta, expense, expense_after_deduction, income, assets,
                                liabilities, saving, json_path)

    book.close()


if __name__ == "__main__":
    main()
