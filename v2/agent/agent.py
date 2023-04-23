import pdb
import re
from prompts import (
    create_plan_prompt,
    plan_next_action_prompt,
    prompt_current_activity,
)
from openai_handler import OpenAIHandler

from colorama import Fore, Back, Style

from helpers import (
    datetime_formatter,
    handle_logging,
    calling_method_name,
    string_from_array,
)

from .agent_utils import previous_day_summary, store_memory

from memory import MemoryObject, MemoryStream


class Agent:
    def __init__(self, biography_data, quick_start_data=None):
        self.memories = []
        self.memory_stream = MemoryStream()
        self.name = biography_data["name"]
        self.innate_tendencies = biography_data["innate_tendencies"]
        self.learned_tendencies = biography_data["learned_tendencies"]
        self.current_datetime = None
        self.next_action = None
        self.age = biography_data["age"]
        self.occupational_statement = biography_data["occupational_statement"]
        self.biography_data = biography_data
        self.seed_memories(biography_data)
        self.cached_agent_summary = None
        self.daily_plan = None
        self.next_hour_plan = None
        if quick_start_data is not None:
            self.daily_plan = quick_start_data["quick_start_daily_plan"]
            self.cached_daily_occupation = quick_start_data["quick_start_occupation"]
            self.cached_core_characteristics = quick_start_data[
                "quick_start_core_characteristics"
            ]

            # self.cached_self_assessment = biography_data["quick_start_self_assessment"],
        else:
            self.cached_daily_occupation = None
            self.cached_core_characteristics = None
            self.cached_self_assessment = None

    def advance_step(self, current_datetime):
        self.current_datetime = current_datetime

        # Make sure there's a plan for the day and next hour
        # if self.daily_plan is None:
        #     self.create_daily_plan()
        #     self.update_next_hour_plan()
        #     self.execute_next_action()

        # if self.should_i_reflect():
        #     self.create_reflection()

        # if self.should_i_plan():
        self.check_daily_plan()
        self.update_next_hour_plan()

        self.determine_next_action()
        self.execute_next_action()
        self.create_observation()

    def current_core_characteristics(self):
        handle_logging(calling_method_name(), type="method")
        if self.cached_core_characteristics is not None:
            return self.cached_core_characteristics
        else:
            core_characteristics = OpenAIHandler.chatCompletion(
                self,
                context=self.biography_data["biography"],
                prompt=self.name + "'s core characteristics.",
            )
            core_characteristics_summary = OpenAIHandler.chatCompletion(
                self,
                "How would one describe "
                + self.name
                + "'s core characteristics given the following statements?\n"
                + core_characteristics,
            )
            self.cached_core_characteristics = core_characteristics_summary
            return core_characteristics_summary

    def current_occupation(self):
        handle_logging(calling_method_name(), type="method")
        if self.cached_daily_occupation is not None:
            return self.cached_daily_occupation
        else:
            occupation = OpenAIHandler.chatCompletion(
                self,
                context=self.biography_data["biography"],
                prompt=self.name + "'s current daily occupation.",
            )
            self.cached_daily_occupation = occupation
            return occupation

    def current_self_assessment(self):
        handle_logging(calling_method_name(), type="method")
        if self.cached_self_assessment is not None:
            return self.cached_self_assessment
        else:
            self_assessment = OpenAIHandler.chatCompletion(
                self,
                context=self.biography_data["biography"],
                prompt=self.name + "'s feeling about his recent progress in life",
            )
            self.cached_self_assessment = self_assessment
            return self_assessment

    def agent_summary(self):
        handle_logging(calling_method_name(), type="method")
        if self.cached_agent_summary is not None:
            return self.cached_agent_summary
        else:
            separator = ","
            tendencies = separator.join(str(item) for item in self.innate_tendencies)
            identity_information = (
                "Name: " + self.name + " (age: " + str(self.age) + ")\n"
            )

            personality = (
                self.name
                + "'s innate tendencies and personality are: "
                + tendencies
                + "\n"
            )

            characteristics = (
                self.name
                + "'s can be described as "
                + self.current_core_characteristics()
                + "\n"
            )
            occupation = (
                self.name
                + "'s current occupation is "
                + self.current_occupation()
                + "\n"
            )
            # self_assessment = self.name + " feels " + self.current_self_assessment()

            # Get the 10 most recent memories
            recent_memories = string_from_array(self.memories[-10:])

            # TODO: Add current_self_assessment
            agent_summary = (
                identity_information
                + personality
                + characteristics
                + occupation
                + recent_memories
                # + self_assessment
            )

            self.cached_agent_summary = agent_summary
            return agent_summary

    def seed_memories(self, seed_data):
        handle_logging(calling_method_name(), type="method")
        self.memories.extend(
            [phrase.strip() for phrase in seed_data["biography"].split(";")]
        )

        # TODO: Enable once pinecone works
        # self.memory_stream.create_and_add_memory(
        #     description=seed_data["biography"], timestamp=self.current_datetime
        # )

    def create_observation(self):
        handle_logging(calling_method_name(), type="method")
        context = self.agent_summary() + string_from_array(self.memories[-10:])

        response = OpenAIHandler.chatCompletion(
            self,
            context=context,
            prompt=prompt_current_activity(
                agent=self,
                current_datetime=self.current_datetime,
            ),
        )

        store_memory(
            self, f"At {datetime_formatter(self.current_datetime)}, {response}."
        )
        handle_logging(
            datetime_formatter(self.current_datetime) + " - " + response,
            type="agent_event",
        )
        return

    def check_daily_plan(self):
        handle_logging(calling_method_name(), type="method")
        if self.daily_plan is not None:
            return self.daily_plan
        else:
            handle_logging("create_plan(daily)", type="method")

            # context = (
            #     datetime_formatter(self.current_datetime)
            #     + self.agent_summary()
            #     + previous_day_summary(self)
            # )

            response = OpenAIHandler.chatCompletion(
                self,
                # context=context,
                prompt=create_plan_prompt(
                    current_datetime=datetime_formatter(self.current_datetime),
                    # yesterday_summary=previous_day_summary(self),
                    agent=self,
                    detail_level="daily",
                ),
            )

            self.daily_plan = response

    def update_next_hour_plan(self):
        handle_logging(calling_method_name(), type="method")

        response = OpenAIHandler.chatCompletion(
            self,
            prompt=create_plan_prompt(
                current_datetime=self.current_datetime,
                agent=self,
                detail_level="hourly",
            ),
        )

        self.next_hour_plan = response

        return response

    def should_i_plan(self):
        handle_logging(calling_method_name(), type="method")

    def should_i_reflect(self):
        handle_logging(calling_method_name(), type="method")
        # last_100_memories = Memory.last(100)
        # number_of_reflections_in_last_100_memories = last_100_memories.where(
        #     type="reflection"
        # ).count()

        # importance_of_memories = 0

        # if number_of_reflections_in_last_100_memories > 0:
        #     return False
        # else:
        #     importance_of_memories = last_100_memories.each(
        #         lambda memory: memory.importance
        #     ).sum(lambda importance: importance)
        #     if importance_of_memories > REFLECTION_THRESHOLD:
        #         return True
        #     else:
        #         return False

    def what_should_i_reflect_on(self):
        handle_logging(calling_method_name(), type="method")
        # name = self.name
        # recent_memories = Memory.where(type="reflection").last(100)  # pseudo code
        # openai_handler_instance = OpenAIHandler.chatCompletion(
        #     prompt=WHAT_SHOULD_I_REFLECT_ON + recent_memories
        # )
        # reflection_questions = openai_handler_instance.response

    def create_reflection(self):
        handle_logging(calling_method_name(), type="method")
        # inputs:
        # questions_to_reflect_on: # one of the questions from what_should_i_reflect_on?
        # retrieved_memories: #retrieve_memories response
        # prompt: # see CREATE_REFLECTION_PROMPT
        # output:

    def retrieve_memories(self):
        handle_logging(calling_method_name(), type="method")

    # inputs:
    #   agent: #self
    #   prompt: #PENDING
    #   recency: #exponential_decay_factor: 0.99
    #   relevancy: (natural_language) #generate an embedding vector of the text description of each memory. Then, we calculate relevance as the cosine similarity between the memory’s embedding vector and the query memory’s embedding vector.
    # outputs: array of retrieved memories

    def prioritize_memories(
        self,
    ):  # normalize the recency, relevance, and importance scores to the range of [0, 1], then sum, then prioritize
        handle_logging(calling_method_name(), type="method")

    # input: retrieved_memories[]
    # output: prioritized_memories[]
    def determine_next_action(self):
        handle_logging(calling_method_name(), type="method")
        # context = self.prioritize_memories()
        response = OpenAIHandler.chatCompletion(
            self,
            prompt=plan_next_action_prompt(
                self.cached_agent_summary,
                agent=self,
                current_datetime=self.current_datetime,
            ),
        )

        self.next_action = response

        return response

    def execute_next_action(self):
        handle_logging(calling_method_name(), type="method")
        store_memory(self, self.next_action)

        return

    # action_talk: (natural_language)
    # action_move: pathing_function
    # action_act_upon_world:
