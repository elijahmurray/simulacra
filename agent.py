from memory import Memory
from environment_objects import Building, Room, RoomObject
from environment_objects import process_room

class Agent:
    def __init__(self, name: str, description: str, starting_location: Room):
        self.name = name
        self.description = description
        self.location = starting_location
        self.memory_stream = [Memory(element) for element in self.description.split(';')]

    def add_memory(self, description: str):
        self.memory_stream.append(Memory(description))

    def observe(self):
        observations = []
        observations.append(f"{self.name} is in the {self.location.name} in the {self.location.building.name}.")
        observations.extend(process_room(self.location))
        for observation in observations:
            self.add_memory(observation)

    def react(self, observation: str):
        pass

    def plan(self):
        pass

    def retrieve_memory(self, query: str):
        pass

    def move_to_room(self, new_location):
        self.location.remove_occupant(self.name)
        self.location = new_location
        new_location.add_occupant(self.name)

    def converse(self, other_agent, message):
        pass


