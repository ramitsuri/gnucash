from utils.account import get_totals_for_accounts, FilterType
from utils.md import print_markdown
from utils.html import print_html
from utils.json_ut import print_json


def print_reports(root_account, config, time_delta, years, json_path, html_path, save_result):
    should_print_html = config['print_html']
    should_print_json = config['print_json']
    should_print_markdown = config['print_markdown']
    file_name_suffix = config['file_name_suffix']
    report_name_suffix = config['report_name_suffix']
    with_running_balance = config['with_running_balance']

    result = {}

    for year in years:
        totals_root = __print_report(root_account, year, time_delta, [], None, should_print_html,
                                     should_print_json, should_print_markdown, json_path, html_path, file_name_suffix,
                                     report_name_suffix, with_running_balance)
        if save_result:
            result[year] = totals_root

    if 'with_filter' in config:
        with_filter = config['with_filter']
    else:
        return result

    filter_accounts = with_filter['exclude_accounts']
    filter_type = FilterType.EXCLUDE
    file_name_suffix = with_filter['file_name_suffix']
    report_name_suffix = with_filter['report_name_suffix']
    with_running_balance = with_filter['with_running_balance']

    for year in years:
        totals_root = __print_report(root_account, year, time_delta, filter_accounts, filter_type,
                                     should_print_html, should_print_json, should_print_markdown, json_path, html_path,
                                     file_name_suffix, report_name_suffix, with_running_balance)
        if save_result:
            result[year] = totals_root

    return result


def __print_report(root_account, year, time_delta, filter_accounts, filter_type, should_print_html, should_print_json,
                   should_print_markdown, json_path, html_path, file_name_suffix, report_name_suffix,
                   with_running_balance):
    # For accounts like liabilities and assets it makes sense to show the running total instead of how much the value
    # changed in a given month. That is what the `with_running_balance` Boolean does.
    # For ex: If CreditCard1 was charged $500 in one month and then for $200 in next month, you would want the total
    # to say that the balance on the card at the end of each month, rather than changes in each month
    # |  ACCOUNT  | MONTH 1 | MONTH 2 |              |  ACCOUNT  | MONTH 1 | MONTH 2 |
    # |-----------|---------|---------|      vs      |-----------|---------|---------|
    # |  CREDIT 1 |   500   |   200   |              |  CREDIT 1 |   500   |   700   |
    #
    # This is controlled by the with_running_balance property and should be set accordingly for Liabilities and Assets
    totals_root = get_totals_for_accounts(root_account, year, time_delta, filter_accounts, filter_type,
                                          with_running_balance=with_running_balance)
    report_name = str(year) + report_name_suffix
    file_name = str(year) + file_name_suffix

    if should_print_html:
        print_html(html_path, report_name, file_name, totals_root)
    if should_print_json:
        print_json(json_path, report_name, file_name, totals_root)
    if should_print_markdown:
        print_markdown(report_name, totals_root)

    return totals_root