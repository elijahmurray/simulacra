class Scheduler:
    def __init__(self):
        self.time = 0

    def step(self, agents):
        self.time += 1
        for agent in agents.values():
            agent.perform_tasks(self.time)
