from enum import Enum


class PrintType(str, Enum):
    HTML = "h"
    JSON = "j"
    MD = "m"
