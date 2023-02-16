from utils.account import get_totals_for_accounts
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(root_account, liabilities_config, time_delta):
    years = liabilities_config['years']

    for year in years:
        __print_report(root_account, year, time_delta)


def __print_report(root_account, year, time_delta):
    html_path = 'output/html/'
    json_path = 'output/json/'

    should_print_html = False
    should_print_json = False
    should_print_markdown = True

    # For accounts like liabilities and assets it makes sense to show the running total instead of how much the value
    # changed in a given month. That is what the `with_running_balance` Boolean does.
    # For ex: If CreditCard1 was charged $500 in one month and then for $200 in next month, you would want the total
    # to say that the balance on the card at the end of each month, rather than changes in each month
    # |  ACCOUNT  | MONTH 1 | MONTH 2 |              |  ACCOUNT  | MONTH 1 | MONTH 2 |
    # |-----------|---------|---------|      vs      |-----------|---------|---------|
    # |  CREDIT 1 |   500   |   200   |              |  CREDIT 1 |   500   |   700   |
    totals_root = get_totals_for_accounts(root_account, year, time_delta, with_running_balance=True)
    report_name = str(year) + "_Liabilities_All"
    if should_print_html:
        print_html(html_path, report_name, totals_root)
    if should_print_json:
        print_json(json_path, report_name, totals_root)
    if should_print_markdown:
        print_markdown(report_name, totals_root)
