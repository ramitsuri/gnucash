from report.utils.account import get_totals_for_accounts, set_balances_on_parents, FilterType, AccountTotal
from report.utils.md import print_markdown
from report.utils.html import print_html
from report.utils.json_ut import print_report
from report.utils.print_type import PrintType


def print_reports(print_types, root_account, config, time_delta, years, json_path, html_path):
    file_name_suffix = "_Savings"
    report_name_suffix = config['report_name_suffix']
    with_running_balance = config['with_running_balance']

    retirement_config = config['retirement']
    brokerage_config = config['brokerage']
    savings_config = config['savings']

    report_account_name = config['report_account_name']
    retirement_account_name = retirement_config['report_account_name']
    brokerage_account_name = brokerage_config['report_account_name']
    savings_account_name = savings_config['report_account_name']

    retirement_accounts = retirement_config['accounts']
    brokerage_accounts = brokerage_config['accounts']
    savings_accounts = savings_config['accounts']
    filter_accounts = retirement_accounts + brokerage_accounts + savings_accounts
    for year in years:
        totals_root = get_totals_for_accounts(root_account, year, time_delta, filter_accounts, FilterType.INCLUDE,
                                              with_running_balance=with_running_balance)
        report_account_total = AccountTotal(report_account_name, report_account_name)
        retirement_account_total = AccountTotal(retirement_account_name, retirement_account_name)
        brokerage_account_total = AccountTotal(brokerage_account_name, brokerage_account_name)
        savings_account_total = AccountTotal(savings_account_name, savings_account_name)

        leaf_accounts = __get_leaf_accounts(totals_root)
        for leaf_account in leaf_accounts:
            if leaf_account.fullname in retirement_accounts:
                retirement_account_total.children.append(leaf_account)
            elif leaf_account.fullname in brokerage_accounts:
                brokerage_account_total.children.append(leaf_account)
            elif leaf_account.fullname in savings_accounts:
                savings_account_total.children.append(leaf_account)

        report_account_total.children.append(retirement_account_total)
        report_account_total.children.append(brokerage_account_total)
        report_account_total.children.append(savings_account_total)

        set_balances_on_parents(report_account_total)

        report_name = str(year) + report_name_suffix
        file_name = str(year) + file_name_suffix

        if PrintType.HTML in print_types:
            print_html(html_path, report_name, file_name, report_account_total)
        if PrintType.JSON in print_types:
            print_report(json_path, report_name, file_name, report_account_total)
        if PrintType.MD in print_types:
            print_markdown(report_name, report_account_total)


def __get_leaf_accounts(root_account_total):
    if not root_account_total.children:
        return [root_account_total]
    leaves = []
    for child in root_account_total.children:
        leaves.extend(__get_leaf_accounts(child))
    return leaves
