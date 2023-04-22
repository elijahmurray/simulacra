import datetime
import agent as Agent

TIME_INCREMENT = 5  # in_minutes


class WorldClock:
    def __init__(self):
        self.start_datetime = self.determine_start_time()
        self.current_datetime = self.start_datetime

    def determine_start_time(self):
        return datetime.datetime.now()

    def advance_time(self, agents):
        print("\nThe time is " + self.datetime_formatter(self.current_datetime))
        for agent in agents:
            agent.step_checker()
        self.current_datetime += datetime.timedelta(minutes=TIME_INCREMENT)

    def datetime_formatter(self, datetime):
        return self.round_time_to_nearest_5_minutes(datetime).strftime("%H:%M")

    def round_time_to_nearest_5_minutes(self, datetime):
        minute = 5 * round(datetime.minute / 5)
        if minute >= 60:
            minute = 0
            datetime = datetime.replace(hour=datetime.hour + 1)
        return datetime.replace(second=0, microsecond=0, minute=minute)
