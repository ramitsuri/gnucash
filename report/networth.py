from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_report
from utils.account import Balance, AccountTotal


def print_reports(liabilities_root_account, assets_root_account, config, years, json_path, html_path):
    should_print_html = config['print_html']
    should_print_json = config['print_json']
    should_print_markdown = config['print_markdown']
    file_name_suffix = config['file_name_suffix']
    report_name_suffix = config['report_name_suffix']
    account_name = config['report_account_name']

    for year in years:
        assets_balances = assets_root_account[year].balances
        liabilities_balances = liabilities_root_account[year].balances

        networth_balances_for_year = []
        month_indices = range(0, 12)
        for month_index in month_indices:
            month_balance = assets_balances[month_index].amount - liabilities_balances[month_index].amount
            networth_balances_for_year.append(Balance(assets_balances[month_index].month, month_balance))

        networth_account_total = AccountTotal(account_name, account_name)
        networth_account_total.balances = networth_balances_for_year

        __print_report(networth_account_total, year, should_print_html, should_print_json, should_print_markdown,
                       json_path, html_path, file_name_suffix, report_name_suffix)


def __print_report(totals_root, year, should_print_html, should_print_json, should_print_markdown,
                   json_path, html_path, file_name_suffix, report_name_suffix):
    report_name = str(year) + report_name_suffix
    file_name = str(year) + file_name_suffix

    if should_print_html:
        print_html(html_path, report_name, file_name, totals_root)
    if should_print_json:
        print_report(json_path, report_name, file_name, totals_root)
    if should_print_markdown:
        print_markdown(report_name, totals_root)
