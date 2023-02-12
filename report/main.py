import json
import piecash

from utils.date import to_time_delta
from utils.account import get_totals_for_accounts, get_totals_for_each_month, filter_out_and_get_totals
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def print_expense_reports(accounts, year, time_delta, exclude_parents, exclude_children):
    account_type = "EXPENSE"
    html_path = 'output/html/'
    json_path = 'output/json/'

    should_print_html = True
    should_print_json = True
    should_print_markdown = False

    # Expense report with all accounts

    totals_for_accounts = get_totals_for_accounts(accounts, account_type, year, time_delta)
    totals_for_each_month = get_totals_for_each_month(totals_for_accounts)
    report_name = str(year) + "_Expenses_All"
    if should_print_html:
        print_html(html_path, report_name, totals_for_accounts, totals_for_each_month)
    if should_print_json:
        print_json(json_path, report_name, totals_for_accounts)
    if should_print_markdown:
        print_markdown(report_name, totals_for_accounts, totals_for_each_month)

    # Expense report without some accounts

    filtered_totals_for_accounts = filter_out_and_get_totals(totals_for_accounts, exclude_parents, exclude_children)
    filtered_totals_for_each_month = get_totals_for_each_month(filtered_totals_for_accounts)
    filtered_report_name = str(year) + "_Expenses_Filtered"
    if should_print_html:
        print_html(html_path, filtered_report_name, filtered_totals_for_accounts, filtered_totals_for_each_month)
    if should_print_json:
        print_json(json_path, filtered_report_name, filtered_totals_for_accounts)
    if should_print_markdown:
        print_markdown(filtered_report_name, filtered_totals_for_accounts, filtered_totals_for_each_month)


def main():
    config = read_config()
    gnu_cash_file = config['file']
    years = config['years']
    time_delta = to_time_delta(config['time_delta_hours'])

    book = piecash.open_book(gnu_cash_file, readonly=True, open_if_lock=True)

    exclude_parents = config['exclude_parents']
    exclude_children = config['exclude_children']
    for year in years:
        print_expense_reports(book.accounts, year, time_delta, exclude_parents, exclude_children)

    book.close()


if __name__ == "__main__":
    main()
