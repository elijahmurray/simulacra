# import MEMORY_IMPORTANCE_PROMPT from 'prompts'

MEMORY_TYPES = ["observation", "plan", "reflection"]


class Memory:
    def __init__(self, name, agent, description_prompt):
        self.name = name
        self.created_at = Datetime.now
        self.last_retrieved_at = Datetime.now
        self.agent = agent
        self.importance = self.generate_importance(self)
        self.description = self.description
        self.type = enumerate[MEMORY_TYPES]

    def generate_description(self):
        response = call_openai(prompt)
        # observation sample description: <Agent> is <active action> [preposition i.e. on/to/with] <environment object OR agent>
        # plan sample output description:
        # reflection sample output description:
        return response

    def generate_importance(self):
        prompt = MEMORY_IMPORTANCE_PROMPT + self.description
        importance = call_openai(prompt)
        return importance

    def call_openai(prompt):
        # stubbed out openAI call
        response = ""
        return response
