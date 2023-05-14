import json
import piecash

from utils.date import to_time_delta
import report
import networth
import savings
import tx
import tx_groups


def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config


def main():
    config = read_config()
    gnu_cash_file = config['file']
    time_delta = to_time_delta(config['time_delta_hours'])

    print_expense = config['print_expense']
    print_income = config['print_income']
    print_networth = config['print_networth']
    print_savings = config['print_savings']
    print_transactions = config['print_transactions']
    print_transaction_groups = config['print_transaction_groups']
    years = config['years']
    json_path = config['json_path']
    html_path = config['html_path']

    book = piecash.open_book(gnu_cash_file, readonly=True, open_if_lock=True)

    account_names = {}
    for account in book.accounts:
        account_names[account.guid] = account.fullname

    # Expense reports
    if print_expense:
        expense_config = config['expense']
        expense_root_account = book.root_account.children(name=expense_config['root_account_name'])
        report.print_reports(expense_root_account, expense_config, time_delta, years, json_path, html_path,
                             save_result=False)

    # Income reports
    if print_income:
        income_config = config['income']
        income_root_account = book.root_account.children(name=income_config['root_account_name'])
        report.print_reports(income_root_account, income_config, time_delta, years, json_path, html_path,
                             save_result=False)

    if print_networth:
        # Assets reports
        assets_config = config['assets']
        assets_root_account = book.root_account.children(name=assets_config['root_account_name'])
        assets = report.print_reports(assets_root_account, assets_config, time_delta, years, json_path, html_path,
                                      save_result=True)

        # Liabilities reports
        liabilities_config = config['liabilities']
        liabilities_root_account = book.root_account.children(name=liabilities_config['root_account_name'])
        liabilities = report.print_reports(liabilities_root_account, liabilities_config, time_delta, years, json_path,
                                           html_path, save_result=True)

        # Networth reports
        networth_config = config['networth']
        networth.print_reports(liabilities, assets, networth_config, years, json_path, html_path)

    # Savings reports
    if print_savings:
        savings_config = config['savings']
        assets_root_account = book.root_account.children(name=savings_config['root_account_name'])
        savings.print_reports(assets_root_account, savings_config, time_delta, years, json_path, html_path)

    # Transactions
    if print_transactions:
        tx_config = config['transactions']
        tx.print_transactions(book.transactions, account_names, years, time_delta, tx_config, json_path)

    # Transaction Groups
    if print_transaction_groups:
        tx_groups_config = config['transaction_groups']
        tx_groups.print_transaction_groups(book.transactions, tx_groups_config, json_path)

    book.close()


if __name__ == "__main__":
    main()
