import pdb
import re
from prompts import (
    WHAT_SHOULD_I_OBSERVE_PROMPT,
    create_plan_prompt,
    what_should_i_do_next_prompt,
)
from APP_CONSTANTS import VERBOSE_MODE
from openai_handler import OpenAIHandler

from colorama import Fore, Back, Style

from helpers import (
    datetime_formatter,
    tuple_or_array_to_string,
    time_formatter,
)

from .agent_utils import (
    print_current_method,
    print_response,
    previous_day_summary,
    store_memory,
)

from memory import MemoryStream


class Agent:
    def __init__(self, biography_data, age=19):
        self.memory_stream = MemoryStream()
        self.name = biography_data["name"]
        self.memories = []
        self.innate_tendencies = biography_data["innate_tendencies"]
        self.learned_tendencies = biography_data["learned_tendencies"]
        self.current_datetime = None
        self.next_action = None
        self.age = age
        self.occupational_statement = biography_data["occupational_statement"]
        self.seed_memories(biography_data)

    def advance_step(self, current_datetime):
        self.current_datetime = current_datetime
        self.create_observation()

        # if self.should_i_reflect():
        #     self.create_reflection()

        # if self.should_i_plan():
        self.create_plan()
        # self.create_plan(detail_level=3)

        self.determine_next_action()
        self.execute_next_action()

    def current_action_statement(self):
        print_current_method(self, "current_action_statement")
        # (natural_language)

    def current_core_characteristics(self):
        core_characteristics = OpenAIHandler.chatCompletion(self.name + "'s core characteristics.")
        core_characteristics_summary = OpenAIHandler.chatCompletion("How would one describe " + self.name + "'s core characteristics given the following statements?\n" + core_characteristics)

        return core_characteristics_summary

    def current_occupation(self):
        # note: may want to summary similar to current_core_characteristics depending on results
        return OpenAIHandler.chatCompletion(self.name + "'s current daily occupation.")

    def current_self_assessment(self):
        # note: may want to summary similar to current_core_characteristics depending on results
        return OpenAIHandler.chatCompletion(self.name + "'s feeling about his recent progress in life")

    
    def agent_summary(self):
        identity_information = "Name: " + self.name + " (age: " + str(self.age) + ")\n"
        personality = self.name + "'s innate tendencies and personality are: " + self.innate_tendencies + "\n"
        characteristics = self.name + "'s can be described as " + self.current_core_characteristics
        occupation = self.name + "'s current occupation is " + self.current_occupation
        self_assessment = self.name + " feels " + self.current_self_assessment

        agent_summary = identity_information + personality + characteristics + occupation + self

        return agent_summary

    def seed_memories(self, seed_data):
        self.memory_stream.create_and_add_memory(description=seed_data["biography"], timestamp=, importance=)

    def create_observation(self):
        print_current_method(self, "create_observation")
        context = self.memories

        response = OpenAIHandler.chatCompletion(
            context=context, prompt=WHAT_SHOULD_I_OBSERVE_PROMPT
        ).response

        store_memory(self, response)
        print_response(
            self,
            "At " + time_formatter(self.current_datetime) + ", " + response,
            color=Fore.WHITE,
        )

    def create_plan(self, higher_level_plan="", detail_level=1):
        print_current_method(self, "create_plan(detail: " + str(detail_level) + ")")

        if detail_level == 1:
            context = (
                datetime_formatter(self.current_datetime)
                + self.agent_summary()
                + previous_day_summary(self)
            )
        if detail_level == 2:
            context = datetime_formatter(
                self.current_datetime
            ) + tuple_or_array_to_string(higher_level_plan)

        response = (
            OpenAIHandler.chatCompletion(
                context=context,
                prompt=create_plan_prompt(
                    current_datetime=datetime_formatter(self.current_datetime),
                    agent_name=self.name,
                    detail_level=detail_level,
                ),
            ).response,
        )

        if VERBOSE_MODE:
            print_response(self, "Plan: ")
            print_response(self, response)

        # TODO: Make this work
        # output_formatter(response)

        if detail_level == 2:
            store_memory(self, response)
            return response
        else:
            self.create_plan(detail_level=2, higher_level_plan=response)

    def should_i_plan(self):
        print_current_method(self, "should_i_plan")

    def should_i_reflect(self):
        print_current_method(self, "should_i_reflect")
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
        print_current_method(self, "what_should_i_reflect_on")
        # name = self.name
        # recent_memories = Memory.where(type="reflection").last(100)  # pseudo code
        # openai_handler_instance = OpenAIHandler.chatCompletion(
        #     prompt=WHAT_SHOULD_I_REFLECT_ON + recent_memories
        # )
        # reflection_questions = openai_handler_instance.response

        # return print_response(self, reflection_questions)

    def create_reflection(self):
        print_current_method(self, "create_reflection")
        # inputs:
        # questions_to_reflect_on: # one of the questions from what_should_i_reflect_on?
        # retrieved_memories: #retrieve_memories response
        # prompt: # see CREATE_REFLECTION_PROMPT
        # output:

    def retrieve_memories(self):
        print_current_method(self, "retrieve_memories")

    # inputs:
    #   agent: #self
    #   prompt: #PENDING
    #   recency: #exponential_decay_factor: 0.99
    #   relevancy: (natural_language) #generate an embedding vector of the text description of each memory. Then, we calculate relevance as the cosine similarity between the memory’s embedding vector and the query memory’s embedding vector.
    # outputs: array of retrieved memories

    def prioritize_memories(
        self,
    ):  # normalize the recency, relevance, and importance scores to the range of [0, 1], then sum, then prioritize
        print("pending")

    # input: retrieved_memories[]
    # output: prioritized_memories[]
    def determine_next_action(self):
        print_current_method(self, "determine_next_action")
        context = self.agent_summary()
        # context = self.prioritize_memories()
        response = OpenAIHandler.chatCompletion(
            context=context,
            prompt=what_should_i_do_next_prompt(self.name, self.current_datetime),
        ).response

        self.next_action = response

        return response

    def execute_next_action(self):
        print_current_method(self, "execute_next_action")
        store_memory(self, self.next_action)

        return

    # action_talk: (natural_language)
    # action_move: pathing_function
    # action_act_upon_world:
