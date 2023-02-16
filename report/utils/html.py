from utils.date import get_month
import locale


def print_html(path, report_name, totals_for_accounts):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    text = """
<html>
    <head>
        <link rel="stylesheet" href="../style.css">
        <title>{report_name}</title>
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
        """.format(report_name=report_name)

    text += __print_tree(totals_for_accounts)

    text += """
        </tbody>
    </table>
</html>
        """
    with open(path + report_name + '.html', 'w') as file:
        file.writelines(text)


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
    text = ''
    text += '<tr>'
    text += '\n'
    text += '<td data-label="Account">' + indent + account_total.name + '</td>'
    text += '\n'

    for balance in account_total.balances:
        month = get_month(balance.month)
        amount = locale.currency(balance.amount, grouping=True)
        text += '<td data-label="' + month + '">' + amount + '</td>'
        text += '\n'
    amount = locale.currency(account_total.total, grouping=True)
    text += '<td data-label="' + 'Total' + '">' + amount + '</td>'
    text += '\n'

    text += '</tr>'
    text += '\n'
    return text
