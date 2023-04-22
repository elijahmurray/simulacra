from memory import Memory
from environment import process_room_objects

class Agent:
    def __init__(self, config: dict, world: dict):
        self.name = config['name']
        self.description = config['description']
        self.location = config['starting_location']
        self.memory_stream = [Memory(element) for element in self.description.split(';')]
        plan = self.plan()
        self.add_memory(plan)

    def add_memory(self, description: str):
        self.memory_stream.append(Memory(description))

    def observe(self, environment: dict, location: str):
        observations = process_room_objects(environment[self.location])

    def react(self, observation: str):
        pass

    def plan(self):
        pass

    def retrieve_memory(self, query: str):
        pass

    def move(self, current_location, destination):
        self.location = destination

    def converse(self, other_agent, message):
        pass


