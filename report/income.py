from utils.account import get_totals_for_accounts
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(accounts, income_config, time_delta):
    years = income_config['years']

    for year in years:
        __print_report(accounts, year, time_delta)


def __print_report(accounts, year, time_delta):
    html_path = 'output/html/'
    json_path = 'output/json/'

    should_print_html = False
    should_print_json = False
    should_print_markdown = True

    totals_for_accounts = get_totals_for_accounts(accounts, year, time_delta)
    report_name = str(year) + "_Income_All"
    if should_print_html:
        print_html(html_path, report_name, totals_for_accounts)
    if should_print_json:
        print_json(json_path, report_name, totals_for_accounts)
    if should_print_markdown:
        print_markdown(report_name, totals_for_accounts)
