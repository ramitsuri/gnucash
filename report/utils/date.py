import calendar
from datetime import datetime, timezone, timedelta


def get_start_date(year, month, time_delta):
    return datetime(year, month, 1, 0, 0, 0, 0, timezone(time_delta)).date()


def get_end_date(year, month, time_delta):
    day = calendar.monthrange(year, month)[1]
    return datetime(year, month, day, 0, 0, 0, 0, timezone(time_delta)).date()


def get_month(month):
    datetime_object = datetime.strptime(str(month), "%m")
    return datetime_object.strftime("%b")


def to_time_delta(hours):
    return timedelta(hours=hours)


def current_utc():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_current_month(time_delta):
    return datetime.now(timezone(time_delta)).month


def is_future_month(year, month, time_delta):
    now = datetime.now(timezone(time_delta))
    if year > now.year:
        return True
    if year < now.year:
        return False
    return month > now.month

