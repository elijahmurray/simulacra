import datetime

def datetime_formatter(datetime: datetime.datetime) -> str:
    return round_time_to_nearest_5_minutes(datetime).strftime("%A, %B %d, %Y %I:%M%p")


def date_formatter(datetime: datetime.datetime) -> str:
    return datetime.strftime("%B %d, %Y")


def hour_formatter(datetime: datetime.datetime) -> str:
    return datetime.strftime("%I:%M %p")


def round_time_to_nearest_5_minutes(datetime: datetime.datetime) -> datetime.datetime:
    minute = 5 * round(datetime.minute / 5)
    if minute >= 60:
        minute = 0
        datetime = datetime.replace(hour=datetime.hour + 1)
    return datetime.replace(second=0, microsecond=0, minute=minute)
