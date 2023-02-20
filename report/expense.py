from utils.account import get_totals_for_accounts
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(root_account, config, time_delta, years, json_path, html_path):
    should_print_html = config['print_html']
    should_print_json = config['print_json']
    should_print_markdown = config['print_markdown']
    file_name_suffix = config['file_name_suffix']
    report_name_suffix = config['report_name_suffix']

    for year in years:
        __print_report(root_account, year, time_delta, should_print_html, should_print_json, should_print_markdown,
                       json_path, html_path, file_name_suffix, report_name_suffix)


def __print_report(root_account, year, time_delta, should_print_html, should_print_json, should_print_markdown,
                   json_path, html_path, file_name_suffix, report_name_suffix):
    totals_root = get_totals_for_accounts(root_account, year, time_delta)
    report_name = str(year) + report_name_suffix
    file_name = str(year) + file_name_suffix

    if should_print_html:
        print_html(html_path, report_name, file_name, totals_root)
    if should_print_json:
        print_json(json_path, report_name, file_name, totals_root)
    if should_print_markdown:
        print_markdown(report_name, totals_root)
