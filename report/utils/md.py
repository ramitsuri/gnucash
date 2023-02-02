import locale


def print_markdown(report_name, totals_for_accounts, totals_for_each_month):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    __print_without_new_line('# ' + report_name)
    __print_without_new_line('\n')
    __print_without_new_line('|**ACCOUNT**|**JAN**|**FEB**|**MAR**|**APR**|**MAY**|**JUN**')
    __print_without_new_line('|**JUL**|**AUG**|**SEP**|**OCT**|**NOV**|**DEC**|**TOTAL**|')
    __print_without_new_line('\n')
    __print_without_new_line('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    __print_without_new_line('\n')
    __print_without_new_line('|')
    __print_account_total(totals_for_each_month, False)
    for account_total in totals_for_accounts:
        __print_without_new_line('|')
        __print_account_total(account_total, False)
        if account_total.children:  # list not empty
            for child in account_total.children:
                __print_without_new_line('|')
                __print_account_total(child, True)


def __print_account_total(account_total, indent):
    if indent:
        __print_without_new_line('- ' + account_total.name)
    else:
        __print_without_new_line(account_total.name)
    __print_without_new_line('|')
    for balance in account_total.balances:
        amount = locale.currency(balance.amount, grouping=True)
        __print_without_new_line(amount)
        __print_without_new_line('|')
    amount = locale.currency(account_total.total, grouping=True)
    __print_without_new_line(amount)
    __print_without_new_line('|')

    __print_without_new_line('\n')


def __print_without_new_line(value):
    print(value, end="")
