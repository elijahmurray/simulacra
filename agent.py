from memory import Memory
from environment_objects import Building, Room, RoomObject
from environment_objects import process_room
from vector_utils import store_memory_in_vectordb
from config import IMPORTANCE_PROMPT, INITIAL_PLAN_PROMPT, PLAN_PROMPT_DAY, PLAN_PROMPT_BLOCK, ACTION_LOCATION_PROMPT
from llm_utils import call_llm
import json
from utils import is_in_time_window
import datetime

class Agent:
    def __init__(self, name: str, age: int, description: str, starting_location: Room, sim_time: datetime.datetime):
        self.name = name
        self.age = age
        self.description = description
        self.location = starting_location
        # This gets set in main.py when the sim starts.
        self.sim_time = sim_time
        # The plan variables will be set inside the init function, initialize to None for now.
        self.current_day_plan = None
        self.current_block_plan = None
        self.current_activity = None
        # The following get set on each loop
        self.current_observations = []

        # Personality and foundational background auto-set to importance score of 10
        print(f"creating starting memories for {self.name}")
        for item in self.description.split(';'):
            self.add_memory(item, "background", 10)
        print(f"creating initial plans for {self.name}")
        # Give the agent a starting daily plan and store it in the vectorDB.
        initial_plan_params = {
            "agent_name": self.name,
            "age": self.age,
            "agent_summary_description": self.description,
        }
        initial_plan = call_llm(INITIAL_PLAN_PROMPT, initial_plan_params, max_tokens=1500)
        print(initial_plan)
        self.current_day_plan = json.loads(initial_plan)
        self.add_memory(initial_plan, "day_plan", 10)

        print(f"creating initial block plans for {self.name}")
        # Give the agent a current block plan and store it in the vectorDB.
        self.plan_block()
        self.current_activity = self.get_current_activity()

    def add_memory(self, description: str, type: str, importance_score: int = None):
        if not importance_score:
            importance_score = call_llm(IMPORTANCE_PROMPT, {'description': description})
        memory = Memory(description, importance_score, type, self.sim_time, self.sim_time)
        store_memory_in_vectordb(self.name, memory)
        return memory

    def observe(self):
        observations = []
        observations.append(f"{self.name} is in the {self.location.name} in the {self.location.building.name}.")
        observations.extend(process_room(self.location))
        self.current_observations = []
        for observation in observations:
            observation_memory = self.add_memory(observation, "observation")
            self.current_observations.append(observation_memory)

    def plan_day(self):
        # Should be triggered at the end of each day for the next day.
        day_plan_params = {
            "agent_name": self.name,
            "age": self.age,
            "agent_summary_description": self.description,
            "yesterday_schedule": self.current_day_plan
        }
        day_plan = call_llm(PLAN_PROMPT_DAY, day_plan_params, max_tokens=1500)
        print(day_plan)
        # Update the day plan with the new day plan.
        self.current_day_plan = json.loads(day_plan)
        self.add_memory(day_plan, "day_plan", 10)

    def plan_block(self):
        # Get the current activity
        current_block = self.get_current_block()
        block_plan_params = {
            "agent_name": self.name,
            "age": self.age,
            "agent_summary_description": self.description,
            "block_schedule": current_block
        }
        block_plan = call_llm(PLAN_PROMPT_BLOCK, block_plan_params, max_tokens=1500)
        print(block_plan)
        self.current_block_plan = json.loads(block_plan)
        self.add_memory(block_plan, "block_plan", 10)

    def determine_activity_location(self, activity):
        location_determination_params = {
            "agent_summary_description": self.description,
            "agent_name": self.name,
            "current_location": self.location,
            "known_locations": "TODO",
            "next_action": activity
        }
        location_determination = call_llm(ACTION_LOCATION_PROMPT, location_determination_params, max_tokens=1000)
        pass

    def react(self):
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

    # HELPER FUNCTIONS
    def get_current_block(self):
        for activity in self.current_day_plan["schedule"]:
            if(is_in_time_window(self.sim_time, activity["start_time"], activity["duration_minutes"])):
                return activity

    def get_current_activity(self):
        for activity in self.current_block_plan["schedule"]:
            if(is_in_time_window(self.sim_time, activity["start_time"], activity["duration_minutes"])):
                return activity

