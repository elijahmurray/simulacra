import datetime
import deprecated_agent as Agent
from helpers import datetime_formatter

from helpers import handle_logging

from config import TIME_INCREMENT


time_offset = datetime.timedelta(hours=-14)
START_TIME = datetime.datetime.now() + time_offset


def always_7am_monday():
    # Get the current date and time
    now = datetime.datetime.now()

    # Calculate the number of days until next Monday
    days_to_monday = (7 - now.weekday()) % 7

    # Set the start time to the next Monday at 7AM
    start_time = datetime.datetime.combine(
        now + datetime.timedelta(days=days_to_monday), datetime.time(hour=7)
    )

    return start_time


# START_TIME = always_7am_monday


class WorldClock:
    def __init__(self):
        self.start_datetime = self.determine_start_time()
        self.current_datetime = self.start_datetime

    def determine_start_time(self):
        return self.round_time(START_TIME)

    def advance_time(self, agents):
        pretty_date_time = datetime_formatter(self.current_datetime)
        handle_logging(f"> World Clock: {pretty_date_time}", "world_event")

        for agent in agents:
            agent.advance_step(self.current_datetime)
        self.current_datetime += datetime.timedelta(minutes=TIME_INCREMENT)

        return self.round_time(self.current_datetime)

    def round_time(self, time):
        minutes = (time.minute // TIME_INCREMENT) * TIME_INCREMENT
        rounded_time = time.replace(minute=minutes, second=0, microsecond=0)
        return rounded_time
