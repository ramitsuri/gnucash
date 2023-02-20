import jsonpickle
from decimal import Decimal
from utils.date import current_utc


def print_json(path, report_name, file_name, root_account_total):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    time = current_utc()
    report = _Report(report_name, time, root_account_total)
    json_string = jsonpickle.encode(report, unpicklable=False)
    with open(path + file_name + '.json', 'w') as file:
        file.writelines(json_string)


class _Report:
    def __init__(self, name, time, account_total):
        self.name = name
        self.time = time
        self.account_total = account_total


class _DecimalHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Decimal, data):
        return str(obj)
