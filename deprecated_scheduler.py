from datetime import datetime, timedelta


class Scheduler:
    def __init__(self, agents, hours_to_run=24):
        self.agents = agents
        for agent in agents:
            agent.scheduler = self

        # Round the current time to the nearest 30-minute mark
        now = datetime.now()
        minutes = (now.minute // 30) * 30
        rounded_time = now.replace(minute=minutes, second=0, microsecond=0)

        self.time = rounded_time
        self.previous_time = self.time  # Initialize previous_time
        self.end_time = self.time + timedelta(hours=hours_to_run)

    def new_day_started(self):
        return self.previous_time.day != self.time.day

    def step(self):
        if self.new_day_started():
            print(f"New day started: {self.time.strftime('%Y-%m-%d')}")
            print("        (\\__/)")
            print("        (o^-^o)")
            print('        z(")(")')
        else:
            print(f"The time is now {self.time.strftime('%H:%M')}.")

        for agent in self.agents:
            agent.step()

        self.previous_time = self.time
        self.time += timedelta(minutes=30)
