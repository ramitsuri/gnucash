from utils.date import get_month
import locale


def print_html(path, report_name, totals_for_accounts, totals_for_each_month):
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    html = """
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
    # write month totals
    html += __print_account_total(totals_for_each_month, False)

    for account_total in totals_for_accounts:
        html += __print_account_total(account_total, False)
        if account_total.children:  # list not empty
            for child in account_total.children:
                html += __print_account_total(child, True)

    html += """
        </tbody>
    </table>
</html>
        """
    with open(path + report_name + '.html', 'w') as file:
        file.writelines(html)


def __print_account_total(account_total, indent):
    html = ''
    html += '<tr>'
    html += '\n'
    if indent:
        html += '<td data-label="Account">' + ' - ' + account_total.name + '</td>'
    else:
        html += '<td data-label="Account">' + account_total.name + '</td>'
    html += '\n'

    for balance in account_total.balances:
        month = get_month(balance.month)
        amount = locale.currency(balance.amount, grouping=True)
        html += '<td data-label="' + month + '">' + amount + '</td>'
        html += '\n'
    amount = locale.currency(account_total.total, grouping=True)
    html += '<td data-label="' + 'Total' + '">' + amount + '</td>'
    html += '\n'

    html += '</tr>'
    html += '\n'
    return html
