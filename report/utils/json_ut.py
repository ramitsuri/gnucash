import jsonpickle
from decimal import Decimal


def print_json(path, report_name, totals_for_accounts):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    report = _Report(report_name, totals_for_accounts)
    json_string = jsonpickle.encode(report, unpicklable=False)
    with open(path + report_name + '.json', 'w') as file:
        file.writelines(json_string)


class _Report:
    def __init__(self, name, account_totals):
        self.name = name
        self.account_totals = account_totals


class _DecimalHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Decimal, data):
        return str(obj)
