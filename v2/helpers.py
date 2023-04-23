from colorama import Fore, Back, Style
import inspect


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


def handle_logging(message, type, force_log=False):
    ENABLE_PROMPT_CONTEXT_LOGGING = False
    ENABLE_PROMPT_LOGGING = False
    ENABLE_WORLD_EVENT_LOGGING = True
    ENABLE_METHOD_CALLED_LOGGING = True
    ENABLE_OPENAI_RESPONSE_LOGGING = False
    ENABLE_AGENT_EVENT_LOGGING = True

    if force_log:
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        return
    if type == "method" and ENABLE_METHOD_CALLED_LOGGING:
        print(
            f"{Fore.RED}\n==========================\nCALLED: {message}\n=========================={Style.RESET_ALL}"
        )
        return
    if type == "prompt" and ENABLE_PROMPT_LOGGING:
        print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
        return
    if type == "context" and ENABLE_PROMPT_CONTEXT_LOGGING:
        print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
        return
    if type == "agent_event" and ENABLE_AGENT_EVENT_LOGGING:
        print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")
        return
    if type == "world_event" and ENABLE_WORLD_EVENT_LOGGING:
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
        return
    if type == "openai_response" and ENABLE_OPENAI_RESPONSE_LOGGING:
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        return
    else:
        return


def calling_method_name():
    # get the frame object of the calling function
    frame = inspect.currentframe().f_back
    # get the code object of the calling function
    code = frame.f_code
    # get the name of the calling function
    name = code.co_name
    return name


def string_from_array(array):
    return "\n".join(array)
