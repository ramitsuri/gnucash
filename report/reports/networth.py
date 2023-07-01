from report.utils.md import print_markdown
from report.utils.html import print_html
from report.utils.json_ut import print_report
from report.utils.account import Balance, AccountTotal
from report.utils.print_type import PrintType


def print_reports(print_types, liabilities_root_account, assets_root_account, config, years, json_path, html_path):
    file_name_suffix = "_NetWorth"
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

        __print_report(networth_account_total, year, print_types, json_path, html_path, file_name_suffix,
                       report_name_suffix)


def __print_report(totals_root, year, print_types, json_path, html_path, file_name_suffix, report_name_suffix):
    report_name = str(year) + report_name_suffix
    file_name = str(year) + file_name_suffix

    if PrintType.HTML in print_types:
        print_html(html_path, report_name, file_name, totals_root)
    if PrintType.JSON in print_types:
        print_report(json_path, report_name, file_name, totals_root)
    if PrintType.MD in print_types:
        print_markdown(report_name, totals_root)
