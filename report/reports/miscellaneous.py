from utils.date import get_current_year, get_current_month, get_previous_year
from decimal import Decimal
from utils.json_ut import print_miscellaneous


class Miscellaneous:
    def __init__(self, income_total, expense_total, expense_after_deduction_total, savings_total, account_balances):
        self.income_total = income_total
        self.expense_total = expense_total
        self.expense_after_deduction_total = expense_after_deduction_total
        self.savings_total = savings_total
        self.account_balances = account_balances


class AccountBalance:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance


def print_reports(config, time_delta, expense, expense_after_deductions, income, asset, liability, saving, json_path):
    account_balances = []
    current_year = get_current_year(time_delta)
    previous_year = get_previous_year(time_delta)
    current_month = get_current_month(time_delta)

    current_month_accounts_config = config['current_year_accounts']

    # Assets
    current_year_root_account_total = asset[current_year]
    for account in current_month_accounts_config['assets']:
        found_account = __find_account(current_year_root_account_total, account['name'])
        if account['current_month']:
            account_balances.append(
                AccountBalance(account['display_name'], found_account.balances[current_month - 1].amount))
        else:
            previous_year_root_account_total = asset[previous_year]
            found_account_previous_year = __find_account(previous_year_root_account_total, account['name'])
            balance = found_account.balances[current_month - 1].amount - found_account_previous_year.balances[11].amount
            account_balances.append(AccountBalance(account['display_name'], balance))

    # Liabilities
    current_year_root_account_total = liability[current_year]
    for account in current_month_accounts_config['liability']:
        found_account = __find_account(current_year_root_account_total, account['name'])
        if account['current_month']:
            account_balances.append(
                AccountBalance(account['display_name'], found_account.balances[current_month - 1].amount))
        else:
            previous_year_root_account_total = asset[previous_year]
            found_account_previous_year = __find_account(previous_year_root_account_total, account['name'])
            balance = found_account.balances[current_month - 1].amount - found_account_previous_year.balances[11].amount
            account_balances.append(AccountBalance(account['display_name'], balance))

    # Savings:Income | Expenses:Income
    expense_savings_config = config['expense_savings']

    current_year_root_income_account_total = income[current_year]
    income_to_exclude_total = Decimal("0.0")
    for account in expense_savings_config['income_accounts_to_exclude']:
        found_account = __find_account(current_year_root_income_account_total, account)
        income_to_exclude_total += found_account.total
    income_total = (current_year_root_income_account_total.total - income_to_exclude_total).copy_abs()

    current_year_root_expense_account_total = expense[current_year]
    expense_total = current_year_root_expense_account_total.total

    current_year_root_expense_after_deductions_account_total = expense_after_deductions[current_year]
    expense_after_deductions_total = current_year_root_expense_after_deductions_account_total.total

    current_year_root_savings_account_total = saving[current_year]
    savings_total = current_year_root_savings_account_total.total

    miscellaneous = Miscellaneous(income_total, expense_total, expense_after_deductions_total, savings_total,
                                  account_balances)
    path = json_path
    file_name = "Miscellaneous"
    print_miscellaneous(path, file_name, miscellaneous)


# Returns AccountTotal
def __find_account(account_total_root, account_total_to_find_name):
    account_to_search_children_of = account_total_root
    route = account_total_to_find_name.split(":")[1:]

    for item in route:
        for child in account_to_search_children_of.children:
            if child.name == item:
                account_to_search_children_of = child
                break

    return account_to_search_children_of


def __remove_parent_prefix__(account_full_name, prefix):
    if account_full_name.startswith(prefix):
        return account_full_name[len(prefix):]
