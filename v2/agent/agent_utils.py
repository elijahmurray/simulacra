from APP_CONSTANTS import VERBOSE_MODE
from colorama import Fore, Back, Style

from helpers import (
    datetime_formatter,
)


def store_memory(self, memory):
    if isinstance(memory, list):
        for m in memory:
            store_memory(self, m)
    if isinstance(memory, tuple):
        for m in memory:
            store_memory(self, m)
    else:
        self.memories.append(memory)


def previous_day_summary(self):
    # TODO: this should be a memory
    return (
        "\nYesterday, on "
        + datetime_formatter(self.current_datetime)
        + ", "
        + self.name
        + " 1) woke up at 7:00AM, 2) went to work at 8:00AM, 3) ate lunch at 12:00PM, 4) went to the gym at 5:00PM, 5) ate dinner at 6:30PM, and 6) went to sleep at 10:00PM."
    )


def print_current_method(self, method):
    if VERBOSE_MODE:
        print(
            f"{Fore.RED}\n==========================\nCALLED: {method}\n=========================={Style.RESET_ALL}"
        )
    else:
        pass


def print_response(self, response, color=Fore.GREEN):
    print(f"\n{response}")
