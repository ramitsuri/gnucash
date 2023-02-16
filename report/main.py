import json
import piecash

from utils.date import to_time_delta
import expense
import income
import assets
import liabilities


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def main():
    config = read_config()
    gnu_cash_file = config['file']
    time_delta = to_time_delta(config['time_delta_hours'])

    book = piecash.open_book(gnu_cash_file, readonly=True, open_if_lock=True)

    # Expense reports
    expense_config = config['expense']
    expense_root_account = book.root_account.children(name="Expenses")
    expense.print_reports(expense_root_account, expense_config, time_delta)

    # Income reports
    income_config = config['income']
    income_root_account = book.root_account.children(name="Income")
    income.print_reports(income_root_account, income_config, time_delta)

    # Assets reports
    assets_config = config['assets']
    assets_root_account = book.root_account.children(name="Assets")
    assets.print_reports(assets_root_account, assets_config, time_delta)

    # Liabilities reports
    liabilities_config = config['liabilities']
    liabilities_root_account = book.root_account.children(name="Liabilities")
    liabilities.print_reports(liabilities_root_account, liabilities_config, time_delta)

    book.close()


if __name__ == "__main__":
    main()
