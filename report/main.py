import json
import piecash

from utils.date import to_time_delta
import report


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def main():
    config = read_config()
    gnu_cash_file = config['file']
    time_delta = to_time_delta(config['time_delta_hours'])

    print_expense = config['print_expense']
    print_income = config['print_income']
    print_assets = config['print_assets']
    print_liabilities = config['print_liabilities']
    years = config['years']
    json_path = config['json_path']
    html_path = config['html_path']

    book = piecash.open_book(gnu_cash_file, readonly=True, open_if_lock=True)

    # Expense reports
    if print_expense:
        expense_config = config['expense']
        expense_root_account = book.root_account.children(name=expense_config['root_account_name'])
        report.print_reports(expense_root_account, expense_config, time_delta, years, json_path, html_path)

    # Income reports
    if print_income:
        income_config = config['income']
        income_root_account = book.root_account.children(name=income_config['root_account_name'])
        report.print_reports(income_root_account, income_config, time_delta, years, json_path, html_path)

    # Assets reports
    if print_assets:
        assets_config = config['assets']
        assets_root_account = book.root_account.children(name=assets_config['root_account_name'])
        report.print_reports(assets_root_account, assets_config, time_delta, years, json_path, html_path)

    # Liabilities reports
    if print_liabilities:
        liabilities_config = config['liabilities']
        liabilities_root_account = book.root_account.children(name=liabilities_config['root_account_name'])
        report.print_reports(liabilities_root_account, liabilities_config, time_delta, years, json_path, html_path)

    book.close()


if __name__ == "__main__":
    main()
