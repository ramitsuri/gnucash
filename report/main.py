import calendar
import json
from datetime import datetime, timezone, timedelta
from decimal import Decimal

import piecash
from piecash import Transaction, Split

import locale

class BalanceInfo: 
    def __init__(self, month, amount):
        self.month = month
        self.amount = amount


class AccountInfo: 
    def __init__(self, account):
        self.account = account
        self.children = []
        self.balances = []


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def get_start_date(year, month, time_delta):
    return datetime(year, month, 1, 0, 0, 0, 0, timezone(time_delta)).date()


def get_end_date(year, month, time_delta):
    day = calendar.monthrange(year, month)[1]
    return datetime(year, month, day, 0, 0, 0, 0, timezone(time_delta)).date()


def build_account_map(accounts, exclude_parents, exclude_children):
    account_infos = []
    completed_children = set()
    for account in accounts:
        if account.type != "EXPENSE":
            continue
        if account.parent.type == "ROOT":
            continue
        if account in completed_children:
            continue
        if any(exclude_parent in account.fullname for exclude_parent in exclude_parents):
            continue
        
        if not account.children: # children empty
            account_infos.append(AccountInfo(account))
        else: 
            account_info = AccountInfo(account)    
            for child in account.children:
                completed_children.add(child)    
                if any(exclude_child in child.fullname for exclude_child in exclude_children):
                    continue
                account_info.children.append(AccountInfo(child))
            account_infos.append(account_info)

    return account_infos


def set_balances_on_accounts(account_infos, year, time_delta):
    for info in account_infos:
        if not info.children: # children empty
            info.balances = get_balances(info.account, year, time_delta)
        else:
            for child in info.children:
                child.balances = get_balances(child.account, year, time_delta)
            info.balances = get_balances_for_parent(info)


def get_balances(account, year, time_delta): 
    balances = []
    months = range(1, 13)
    for month in months: 
        balances.append(BalanceInfo(month, get_balance(account, year, month, time_delta)))
    return balances    


def get_balances_for_parent(parent_account_info): 
    balances = []
    months = range(1, 13)
    for month in months: 
        child_sum = Decimal("0.0")
        for child in parent_account_info.children:
            child_sum += child.balances[month - 1].amount
        balances.append(BalanceInfo(month, child_sum))
    return balances    


def get_balance(account, year, month, time_delta):
    start_date = get_start_date(year, month, time_delta)
    end_date = get_end_date(year, month, time_delta)
    amount = Decimal("0.0")
    for acc_split in account.splits:
        if acc_split.transaction.post_date >= start_date and acc_split.transaction.post_date <= end_date:
            for split in acc_split.transaction.splits:
                if split.account.name == account.name:
                    amount += split.value
    return amount 


def get_month(month):
    if month == -1:
        return "Total"
    datetime_object = datetime.strptime(str(month), "%m")
    return datetime_object.strftime("%b")


def calculate_totals(account_infos):
    month_totals = []
    # calculate totals column (per account)
    for info in account_infos:
        info_total = Decimal("0.0")
        for balance in info.balances:
            info_total += balance.amount
        info.balances.append(BalanceInfo(-1, info_total))    
        if info.children: # list not empty
            for child in info.children:
                child_total = Decimal("0.0")
                for balance in child.balances:
                    child_total += balance.amount
                child.balances.append(BalanceInfo(-1, child_total))    

    # calculate totals row (per month)
    for index in range(0, 13): # 0-11 for months, 12 for totals. end number is not included in range
        month_totals.append(Decimal("0.0"))
    for info in account_infos:
        index = 0
        for balance in info.balances:
            month_totals[index] = month_totals[index] + balance.amount
            index += 1
    return month_totals


def write_html_report_for_account(file, account_info, indent):
    file.write('<tr>')
    file.write('\n')
    if indent: 
        file.write('<td data-label="Account">' + ' - ' + account_info.account.name + '</td>')
    else:     
        file.write('<td data-label="Account">' + account_info.account.name + '</td>')
    file.write('\n')

    for balance in account_info.balances:
        file.write('<td data-label="' + get_month(balance.month) + '">' + locale.currency(balance.amount, grouping=True) + '</td>')
        file.write('\n')

    file.write('</tr>')
    file.write('\n')


def write_html_report(month_totals, report_name, account_infos): 
    initial_html1 = """
<html>
<head>
<link rel="stylesheet" href="../style.css">
"""

    initial_html2 = """
</head>
<table>
<thead>
<tr>
<th scope="col">Account</th>
<th scope="col">Jan</th>
<th scope="col">Feb</th>
<th scope="col">Mar</th>
<th scope="col">Apr</th>
<th scope="col">May</th>
<th scope="col">Jun</th>
<th scope="col">Jul</th>
<th scope="col">Aug</th>
<th scope="col">Sep</th>
<th scope="col">Oct</th>
<th scope="col">Nov</th>
<th scope="col">Dec</th>
<th scope="col">Total</th>
</tr>
</thead>
<tbody>
"""
    with open('output/reports/' + report_name + '.html', 'w') as file: 
        file.writelines(initial_html1)
        file.write('\n')
        file.write('<title>' + report_name + '</title>')
        file.write('\n')
        file.writelines(initial_html2)
        # write month totals
        file.write('<tr>')
        file.write('\n')
        file.write('<td data-label="Account">Total</td>')
        file.write('\n')

        for amount in month_totals:
            file.write('<td data-label="' + get_month(-1) + '">' + locale.currency(amount, grouping=True) + '</td>')
            file.write('\n')
        file.write('</tr>')
        file.write('\n')

        # write rest of the accounts 
        for account_info in account_infos:
            write_html_report_for_account(file, account_info, False)
            if account_info.children: # list not empty
                for child in account_info.children:
                    write_html_report_for_account(file, child, True)

        file.write('\n')
        file.write('</tbody>')
        file.write('\n')
        file.write('</table>')
        file.write('\n')
        file.write('</html>')

def debug_print_accounts(account_infos): 
    for account_info in account_infos:
        print(account_info.account.fullname)
        if account_info.children: 
            for child in account_info.children:
                print("     " + child.account.fullname)

def main():
    locale.setlocale(locale.LC_ALL, '')
    config = read_config()
    book = piecash.open_book(config['file'], readonly=True, open_if_lock=True)

    # Expense report with all accounts 
    account_infos_all = build_account_map(book.accounts, exclude_parents = [], exclude_children = [])
    set_balances_on_accounts(account_infos_all, config['year'], timedelta(hours=config['time_delta_hours']))
    month_totals_all = calculate_totals(account_infos_all)
    write_html_report(month_totals_all, str(config['year']) + "_Expenses_All", account_infos_all)
    
    # Expense report without some accounts
    account_infos_filtered = build_account_map(book.accounts, exclude_parents = config['exclude_parents'], exclude_children = config['exclude_children'])
    set_balances_on_accounts(account_infos_filtered, config['year'], timedelta(hours=config['time_delta_hours']))
    month_totals_filtered = calculate_totals(account_infos_filtered)
    write_html_report(month_totals_filtered, str(config['year']) + "_Expenses_Filtered", account_infos_filtered)
    
    book.close()

if __name__ == "__main__":
    main()