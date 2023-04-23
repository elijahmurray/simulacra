from memory import Memory
from environment_objects import Building, Room, RoomObject
from environment_objects import process_room
from vector_utils import store_memory_in_vectordb
from config import IMPORTANCE_PROMPT
from llm_utils import call_llm, get_embedding

class Agent:
    def __init__(self, name: str, description: str, starting_location: Room):
        self.name = name
        self.description = description
        self.location = starting_location
        # Personality and foundational background auto-set to importance score of 10
        self.memory_stream = [Memory(element, 10) for element in self.description.split(';')]

    def add_memory(self, description: str):
        #importance_score = call_llm(IMPORTANCE_PROMPT, {'description': description})
        importance_score = 1
        memory = Memory(description, importance_score)
        self.memory_stream.append(memory)
        store_memory_in_vectordb(self.name, memory)

    def observe(self):
        observations = []
        observations.append(f"{self.name} is in the {self.location.name} in the {self.location.building.name}.")
        observations.extend(process_room(self.location))
        for observation in observations:
            print(observation)
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

    def interact_with_object(self, object):
        pass


