from memory import Memory
from environment_objects import Building, Room, RoomObject
from environment_objects import process_room
from vector_utils import store_memory_in_vectordb
from config import IMPORTANCE_PROMPT, INITIAL_PLAN_PROMPT
from llm_utils import call_llm

class Agent:
    def __init__(self, name: str, age: int, description: str, starting_location: Room):
        self.name = name
        self.age = age
        self.description = description
        self.location = starting_location
        # Personality and foundational background auto-set to importance score of 10
        for item in self.description.split(';'):
            memory = Memory(item, 10, type="background")
            store_memory_in_vectordb(self.name, memory)
        # Give the agent a starting daily plan and store it in the vectorDB.
        initial_plan_params = {
            "agent_name": self.name,
            "age": self.age,
            "agent_summary_description": self.description,
        }
        initial_plan = call_llm(INITIAL_PLAN_PROMPT, initial_plan_params)
        self.daily_plan = initial_plan
        initial_plan_memory = Memory(initial_plan, 10, type="day_plan")
        store_memory_in_vectordb(self.name, initial_plan_memory)

    def add_memory(self, description: str, type: str = "observation"):
        importance_score = call_llm(IMPORTANCE_PROMPT, {'description': description})
        memory = Memory(description, importance_score, type)
        store_memory_in_vectordb(self.name, memory)

    def observe(self):
        observations = []
        observations.append(f"{self.name} is in the {self.location.name} in the {self.location.building.name}.")
        observations.extend(process_room(self.location))
        for observation in observations:
            self.add_memory(observation)

    def react(self):
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


