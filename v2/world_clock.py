import datetime
import agent as Agent
from helpers import datetime_formatter

from helpers import handle_logging


TIME_INCREMENT = 30  # in_minutes
time_offset = datetime.timedelta(hours=+14)
START_TIME = datetime.datetime.now() + time_offset


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
