from memory import Memory
from environment_objects import Building, Room, RoomObject
from environment_objects import process_room
from vector_utils import store_memory_in_vectordb, get_all_memories, update_last_accessed
from config import IMPORTANCE_PROMPT, INITIAL_PLAN_PROMPT, PLAN_PROMPT_DAY, PLAN_PROMPT_BLOCK, ACTION_LOCATION_PROMPT, RETRIEVAL_WEIGHTS, PLAN_REACTION_PROMPT, REFLECTION_PROMPT, REFLECTION_QUESTIONS_PROMPT
from llm_utils import call_llm, get_embedding
import json
from utils import is_in_time_window, extract_json
import datetime
from scipy.spatial.distance import cosine
from typing import List

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
        self.environment = None
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
        #print(initial_plan)
        self.current_day_plan = extract_json(initial_plan)
        self.add_memory(initial_plan, "day_plan", 10)

        print(f"creating initial block plans for {self.name}")
        # Give the agent a current block plan and store it in the vectorDB.
        self.plan_block()
        self.current_activity = self.get_current_activity()

    # LOOP FUNCTIONS

    def process_game_step(self):
        if self.sim_time.hour == 0:
            self.plan_day()
        elif self.sim_time.minute == 0:
            self.plan_block()
        # Observe surroundings and add to memory stream
        self.observe()
        self.reflect()
        # Determine where the next activity should be
        self.current_activity = self.get_current_activity()
        new_location = self.determine_activity_location(self.current_activity)
        self.move_to_room(new_location)

    # PLANNING FUNCTIONS

    def plan_day(self):
        # Should be triggered at the end of each day for the next day.
        day_plan_params = {
            "agent_name": self.name,
            "age": self.age,
            "agent_summary_description": self.description,
            "yesterday_schedule": self.current_day_plan
        }
        day_plan = call_llm(PLAN_PROMPT_DAY, day_plan_params, max_tokens=1500)
        #print(day_plan)
        # Update the day plan with the new day plan.
        self.current_day_plan = extract_json(day_plan)
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
        #print(block_plan)
        self.current_block_plan = extract_json(block_plan)
        self.add_memory(block_plan, "block_plan", 10)

    def determine_activity_location(self, activity):
        location_determination_params = {
            "agent_summary_description": self.description,
            "agent_name": self.name,
            "current_location": str(self.location),
            "current_location_description": [str(observation) for observation in self.current_observations],
            "known_locations": self.get_all_rooms(),
            "next_action": activity
        }
        location_determination = call_llm(ACTION_LOCATION_PROMPT, location_determination_params, max_tokens=200)
        location_determination = extract_json(location_determination)
        new_location = self.room_string_to_room_object(location_determination["location"])
        #print(new_location)
        return new_location

    def react(self):
        # Get most important observation in the list of current observations
        most_important_observation = str(self.current_observations[0])
        # Get relevant context
        relevant_context = self.get_relevant_context(most_important_observation)
        plan_reaction_params = {
            "agent_summary_description": self.description,
            "datetime": str(self.sim_time),
            "agent_name": self.name,
            "current_activity": self.current_activity["description"],
            "observaton": most_important_observation,
            "relevant_context": relevant_context
        }
        plan_reaction = call_llm(PLAN_REACTION_PROMPT, plan_reaction_params, max_tokens=200)
        return plan_reaction

    # INTERTACTION FUNCTIONS

    def observe(self):
        observations = []
        observations.append(f"{self.name} is in the {self.location.name} in the {self.location.building.name}.")
        observations.extend(process_room(self.location))
        self.current_observations = []
        for observation in observations:
            observation_memory = self.add_memory(observation, "observation")
            self.current_observations.append(observation_memory)
        # Store the list of observations sorted by importance score for quick retrieval
        self.current_observations = sorted(self.current_observations, key=lambda x: x.importance_score, reverse=True)

    def move_to_room(self, new_location):
        self.location.remove_occupant(self.name)
        self.location = new_location
        self.location.add_occupant(self.name)

    def generate_dialogue(self, other_agent):

        pass

    def interact_with_object(self, object):
        pass

    # MEMORY AND RETRIEVAL FUNCTIONS

    def add_memory(self, description: str, type: str, importance_score: int = None):
        if not importance_score:
            importance_score = call_llm(IMPORTANCE_PROMPT, {'description': description})
        memory = Memory(description, type, float(importance_score), self.sim_time, self.sim_time)
        store_memory_in_vectordb(self.name, memory)
        return memory

    def get_relevant_context_summary(self, observation: str, n: int = 3):
        relative_memories = self.retrieve_relevant_memories(self.name, f"Whaat is {self.name}'s relationship with the following observation: {observation}?")
        return [mem["description"] for mem in relative_memories[:n]]

    def retrieve_recent_memories(self, n: int = 50):
        memories = get_all_memories(self.name)
        sorted_memories = sorted(memories, key=lambda k: k["last_accessed"], reverse=True)
        top_memories = sorted_memories[:n]
        #memory_objects = [Memory(memory["description"], memory["type"], memory["importance_score"], memory["created_at"], memory["last_accessed"]) for memory in top_memories]
        return top_memories

    def retrieve_relevant_memories(self, query: str, n: int = 10):
        # Get all memories for agent
        memories = get_all_memories(self.name)
        query_embedding = get_embedding(query)

        def calculate_relevance_score(memory_embedding: List, query_embedding: List) -> float:
            return cosine(memory_embedding, query_embedding)

        def calculate_recency_score(last_accessed: datetime.datetime) -> float:
            hours_since_accessed = (self.sim_time - last_accessed).total_seconds() / 3600
            decay_factor = 0.99
            recency_score = decay_factor ** hours_since_accessed
            return recency_score

        # Add the raw scores to the dict so we can do min-max normalization on all three scores
        for memory in memories:
            memory["relevance_score"] = calculate_relevance_score(memory["embedding"], query_embedding)
            memory["recency_score"] = calculate_recency_score(memory["last_accessed"])

        # Normalize the scores
        relevance_scores = [memory["relevance_score"] for memory in memories]
        recency_scores = [memory["recency_score"] for memory in memories]
        importance_scores = [memory["importance_score"] for memory in memories]
        min_relevance = min(relevance_scores)
        max_relevance = max(relevance_scores)
        min_recency = min(recency_scores)
        max_recency = max(recency_scores)
        min_importance = min(importance_scores)
        max_importance = max(importance_scores)

        for memory in memories:
            # relevance must be inverted
            memory["relevance_score"] = 1.0 - ((memory["relevance_score"] - min_relevance) / (max_relevance - min_relevance))
            try:
                memory["recency_score"] = (memory["recency_score"] - min_recency) / (max_recency - min_recency)
            except ZeroDivisionError:
                memory["recency_score"] = 1.0
            memory["importance_score"] = (memory["importance_score"] - min_importance) / (max_importance - min_importance)
            memory["retrieval_score"] = (memory["relevance_score"] * RETRIEVAL_WEIGHTS["relevance"]) + (memory["recency_score"] * RETRIEVAL_WEIGHTS["recency"]) + (memory["importance_score"] * RETRIEVAL_WEIGHTS["importance"])

        sorted_memories = sorted(memories, key=lambda k: k["retrieval_score"], reverse=True)

        relevant_memories = sorted_memories[:n]

        update_last_accessed(self.name, self.sim_time, relevant_memories)

        return relevant_memories

    def reflect(self):
        reflection_questions_params = {
            "recent_memories": [memory["description"] for memory in self.retrieve_recent_memories()],
        }
        reflection_questions = call_llm(REFLECTION_QUESTIONS_PROMPT, reflection_questions_params, max_tokens=500)
        reflection_questions = extract_json(reflection_questions)["questions"]
        statements = []
        for question in reflection_questions:
            relevant_memories = [memory["description"] for memory in self.retrieve_relevant_memories(question, n=3)]
            statements.extend(relevant_memories)
        print(statements)
        reflection_params = {
            "agent_name": self.name,
            "statements": statements
        }
        reflection = call_llm(REFLECTION_PROMPT, reflection_params, max_tokens=500)
        reflection = extract_json(reflection)["insights"]
        print(reflection)
        return reflection

    # HELPER FUNCTIONS

    def get_current_block(self):
        for activity in self.current_day_plan["schedule"]:
            if(is_in_time_window(self.sim_time, activity["start_time"], activity["duration_minutes"])):
                return activity

    def get_current_activity(self):
        for activity in self.current_block_plan["schedule"]:
            if(is_in_time_window(self.sim_time, activity["start_time"], activity["duration_minutes"])):
                return activity

    def get_all_buildings(self):
        return self.environment.keys()

    def get_all_rooms(self):
        rooms = []
        buildings = self.get_all_buildings()
        for building in buildings:
            for room in self.environment[building].rooms.keys():
                rooms.append(f"{room} in {building}")
        return rooms

    def room_string_to_room_object(self, room_string: str):
        elements = room_string.split(" in ")
        room_name = elements[0]
        building_name = elements[1]
        return self.environment[building_name].rooms[room_name]

