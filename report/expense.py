from utils.account import get_totals_for_accounts, get_totals_for_each_month, filter_out_and_get_totals
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(accounts, years, time_delta, exclude_parents, exclude_children):
    for year in years:
        __print_report(accounts, year, time_delta, exclude_parents, exclude_children)


def __print_report(accounts, year, time_delta, exclude_parents, exclude_children):
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
