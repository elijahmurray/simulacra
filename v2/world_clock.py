import datetime
import agent as Agent
from helpers import datetime_formatter
from APP_CONSTANTS import DEBUG_CONTEXT


TIME_INCREMENT = 60  # in_minutes
# START_TIME = datetime.datetime.now()
START_TIME = datetime.datetime.now() + datetime.timedelta(hours=4.5)


class WorldClock:
    def __init__(self):
        self.start_datetime = self.determine_start_time()
        self.current_datetime = self.start_datetime

    def determine_start_time(self):
        return START_TIME

    def advance_time(self, agents):
        pretty_date_time = datetime_formatter(self.current_datetime)
        if DEBUG_CONTEXT:
            print("\n> World Clock: " + pretty_date_time)
        for agent in agents:
            agent.step_checker(self.current_datetime)
        self.current_datetime += datetime.timedelta(minutes=TIME_INCREMENT)
