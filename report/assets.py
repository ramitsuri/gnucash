from utils.account import get_totals_for_accounts
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(root_account, assets_config, time_delta):
    years = assets_config['years']

    for year in years:
        __print_report(root_account, year, time_delta)


def __print_report(root_account, year, time_delta):
    html_path = 'output/html/'
    json_path = 'output/json/'

    should_print_html = True
    should_print_json = True
    should_print_markdown = False

    totals_root = get_totals_for_accounts(root_account, year, time_delta, with_running_balance=True)
    report_name = str(year) + "_Assets_All"
    if should_print_html:
        print_html(html_path, report_name, totals_root)
    if should_print_json:
        print_json(json_path, report_name, totals_root)
    if should_print_markdown:
        print_markdown(report_name, totals_root)
