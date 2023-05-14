from typing import List, Dict
import datetime

class Agent:
    def __init__(self, bio_data: Dict, sim_time: datetime.datetime) -> None:

        # Variables from agent json
        self.name = bio_data["name"]
        self.age = bio_data["age"]
        self.innate_tendencies = bio_data["innate_tendencies"]
        self.location = None
        self.sim_time = sim_time
        self.seed_memories = bio_data["description"].split(";")

        # Variables derived infrequently from llm calls and cached. Initialize as empty.
        self.cached_day_plan = None
        self.cached_hourly_plan = None
        self.cached_current_action = None
        self.cached_current_observations = []

        # Variables derived infrequently from long term memory and cached. Initialize as empty.
        self.cached_learned_tendency = None
        self.cached_occupation = None
        self.cached_lifestyle = None

    # AM functions, merge later

    def process_step():
        pass

    def plan_day():
        pass

    def plan_hour():
        pass

    def determine_action_location():
        pass

    def observe():
        pass

    def react():
        pass

    def move():
        pass

    def generate_dialogue():
        pass

    def get_current_hour():
        pass

    def get_current_action():
        pass
