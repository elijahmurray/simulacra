from PROMPTS_CONSTANTS import BIOGRAPHICAL_MEMORY_1, WHAT_SHOULD_I_REFLECT_ON
import openai_handler
import memory as Memory


class Agent:
    def __init__(self, name):
        self.name = name
        self.biography = self.create_biographical_memory(BIOGRAPHICAL_MEMORY_1)

    def step_checker(self):
        self.create_observation

        if self.should_i_reflect:
            self.create_reflection

        if self.should_i_plan:
            self.create_plan

        self.determine_next_action

    def create_current_action_statement():
        print("pending")
        # (natural_language)

    def create_biographical_memory(biography):
        memories = biography.split
        return openai_handler(prompt=memories)

    def create_observation():
        print("pending")
        # (natural_language)

    def create_plan():
        print("pending")
        # (natural_language)

    def should_i_plan():
        print("pending")

    def should_i_reflect():
        print("pending")
        # trigger:
        # if memory[where type='reflection'].last.index > memory.most_recent.index - 100
        # importance_of_memories = 0
        # memories_to_evaluate.each(memory) {importance_of_memories += memory.importance}
        # if importance_of_memories > REFLECTION_THRESHOLD then TRUE else FALSE
        # output: [boolean]

    def what_should_i_reflect_on(self):
        name = self.name
        recent_memories = Memory.where(type="reflection").last(100)  # pseudo code
        reflection_questions = openai_handler(
            WHAT_SHOULD_I_REFLECT_ON + recent_memories
        )

        return reflection_questions

    def create_reflection():
        print("pending")
        # inputs:
        # questions_to_reflect_on: # one of the questions from what_should_i_reflect_on?
        # retrieved_memories: #retrieve_memories response
        # prompt: # see CREATE_REFLECTION_PROMPT
        # output:

    def retrieve_memories():
        print("pending")

    # inputs:
    #   agent: #self
    #   prompt: #PENDING
    #   recency: #exponential_decay_factor: 0.99
    #   relevancy: (natural_language) #generate an embedding vector of the text description of each memory. Then, we calculate relevance as the cosine similarity between the memory’s embedding vector and the query memory’s embedding vector.
    # outputs: array of retrieved memories
    def prioritize_memories():  # normalize the recency, relevance, and importance scores to the range of [0, 1], then sum, then prioritize
        print("pending")

    # input: retrieved_memories[]
    # output: prioritized_memories[]
    def determine_next_action():
        print("pending")

    # inputs: prioritized_memories[0..10]
    # outputs: (natural_language)
    # action_talk: (natural_language)
    # action_move: pathing_function
    # action_act_upon_world:
