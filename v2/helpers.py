def datetime_formatter(datetime):
    return round_time_to_nearest_5_minutes(datetime).strftime("%A, %B %d, %Y %I:%M%p")


def date_formatter(datetime):
    return datetime.strftime("%B %d, %Y")


def round_time_to_nearest_5_minutes(datetime):
    minute = 5 * round(datetime.minute / 5)
    if minute >= 60:
        minute = 0
        datetime = datetime.replace(hour=datetime.hour + 1)
    return datetime.replace(second=0, microsecond=0, minute=minute)


def tuple_or_array_to_string(tuple_or_array):
    return str(tuple_or_array).replace("(", "").replace(")", "").replace(",", "")


def time_formatter(datetime):
    return datetime.strftime("%I:%M%p")


def output_formatter(response):
    formatted_output = ""

    if isinstance(response, tuple) or isinstance(response, list):
        for r in response:
            formatted_output += "\n" + r
    elif isinstance(response, str):
        formatted_output = response
    else:
        formatted_output = str(response)

    return formatted_output
