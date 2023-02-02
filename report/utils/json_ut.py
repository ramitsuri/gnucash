import jsonpickle
from decimal import Decimal


def print_json(path, report_name, totals_for_accounts):
    jsonpickle.handlers.registry.register(Decimal, _DecimalHandler)
    json_string = jsonpickle.encode(totals_for_accounts, unpicklable=False)
    with open(path + report_name + '.json', 'w') as file:
        file.writelines(json_string)


class _DecimalHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: Decimal, data):
        return str(obj)
