class Scheduler:
    def __init__(self, agents):
        self.agents = agents
        self.time = 0

    def step(self):
        for agent in self.agents:
            agent.perform_tasks(self.time)  # Pass the current time
        self.time += 1
