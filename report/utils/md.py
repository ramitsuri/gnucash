import locale


def print_markdown(report_name, totals_for_accounts):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    text = ''
    text += '# ' + report_name
    text += '\n'
    text += '|**ACCOUNT**|**JAN**|**FEB**|**MAR**|**APR**|**MAY**|**JUN**'
    text += '|**JUL**|**AUG**|**SEP**|**OCT**|**NOV**|**DEC**|**TOTAL**|'
    text += '\n'
    text += '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|'
    text += '\n'

    text += __print_tree(totals_for_accounts)

    print(text)


def __print_tree(root_account_total, level=0):
    text = ''
    text += __print_row(root_account_total, level)
    text += '\n'
    for account_total in root_account_total.children:
        text += __print_tree(account_total, level + 1)
    return text


def __print_row(account_total, level):
    if level <= 1:
        indent = ''
    else:
        indent = ('  ' * (level - 2)) + '- '
    text = '|'
    text += indent + account_total.name
    text += '|'

    for balance in account_total.balances:
        amount = locale.currency(balance.amount, grouping=True)
        text += amount
        text += '|'
    amount = locale.currency(account_total.total, grouping=True)
    text += amount
    text += '|'
    return text
