import json
import piecash

from utils.date import to_time_delta
import expense


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
    years = expense_config['years']
    exclude_parents = expense_config['exclude_parents']
    exclude_children = expense_config['exclude_children']
    expense.print_reports(book.accounts, years, time_delta, exclude_parents, exclude_children)

    book.close()


if __name__ == "__main__":
    main()
