import json
import piecash

from utils.date import to_time_delta
import expense
import income


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
    expenses = book.root_account.children(name="Expenses")
    expense.print_reports(expenses, expense_config, time_delta)

    # Income reports
    income_config = config['income']
    incomes = book.root_account.children(name="Income")
    income.print_reports(incomes, income_config, time_delta)

    book.close()


if __name__ == "__main__":
    main()
