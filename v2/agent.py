from PROMPTS_CONSTANTS import (
    BIOGRAPHICAL_MEMORY_1,
    WHAT_SHOULD_I_REFLECT_ON_PROMPT,
    WHAT_SHOULD_I_OBSERVE_PROMPT,
    WHAT_SHOULD_I_DO_NEXT_PROMPT,
)
from APP_CONSTANTS import VERBOSE_MODE
from openai_handler import OpenAIHandler

import memory as Memory


class Agent:
    def __init__(self, name):
        self.name = name
        self.memories = []
        self.biography = self.create_biographical_memory(BIOGRAPHICAL_MEMORY_1)

    def step_checker(self):
        self.create_observation()

        # if self.should_i_reflect():
        #     self.create_reflection()

        # if self.should_i_plan():
        #     self.create_plan()

        self.determine_next_action()

    def create_current_action_statement(self):
        print("pending")
        # (natural_language)

    def create_biographical_memory(self, biography):
        seed_memories = biography
        self.memories = self.memories + seed_memories

    def create_observation(self):
        self.print_current_method("create_observation")
        context = self.memories

        response = OpenAIHandler(
            context=context, prompt=WHAT_SHOULD_I_OBSERVE_PROMPT
        ).response
        self.store_memory(response)
        self.print_response(response)

    def create_plan(self):
        print("pending")
        # (natural_language)

    def should_i_plan(self):
        print("pending")

    def should_i_reflect(self):
        self.print_current_method("should_i_reflect")
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
        self.print_current_method("what_should_i_reflect_on")
        # name = self.name
        # recent_memories = Memory.where(type="reflection").last(100)  # pseudo code
        # openai_handler_instance = OpenAIHandler(
        #     prompt=WHAT_SHOULD_I_REFLECT_ON + recent_memories
        # )
        # reflection_questions = openai_handler_instance.response

        # return self.print_response(reflection_questions)

    def create_reflection(self):
        self.print_current_method("create_reflection")
        # inputs:
        # questions_to_reflect_on: # one of the questions from what_should_i_reflect_on?
        # retrieved_memories: #retrieve_memories response
        # prompt: # see CREATE_REFLECTION_PROMPT
        # output:

    def retrieve_memories(self):
        self.print_current_method("retrieve_memories")

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
        self.print_current_method("determine_next_action")
        context = self.memories
        # context = self.prioritize_memories()
        response = OpenAIHandler(
            context=context, prompt=WHAT_SHOULD_I_DO_NEXT_PROMPT
        ).response

        if VERBOSE_MODE:
            self.print_response("Next Action Determined: " + response)

        return response

    # inputs: prioritized_memories[0..10]
    # outputs: (natural_language)
    # action_talk: (natural_language)
    # action_move: pathing_function
    # action_act_upon_world:

    def print_current_method(self, method):
        if VERBOSE_MODE:
            print(f"\n==========================\n{method}\n==========================")
        else:
            pass

    def print_response(self, response):
        if VERBOSE_MODE:
            print(f"\nAPI Response - {response}")
        else:
            print(f"\n{response}")

    def store_memory(self, memory):
        self.memories.append(memory)
