import openai

class Agent:
    def __init__(self, name, personality=None):
        self.name = name
        self.memories = []
        self.personality = personality if personality else {"friendliness": 0.5, "formality": 0.5}
        self.current_action = None
        self.tasks = []
        self.experiences = []
        self.relationships = {}
        self.add_memory(f"My name is {name}")

    def generate_conversation_content(self, other_agent):
        prompt = "Generate a conversation between {self.name} and {other_agent.name} based on their personalities, memories, tasks, and shared experiences: {self.personality}, {other_agent.personality}, {self.memories}, {other_agent.memories}, {self.tasks}, {other_agent.tasks}, {self.experiences}, {other_agent.experiences}."
        content = self.generate_response(prompt)
        return content
    
    def talk(self, other_agent):
        content = self.generate_conversation_content(other_agent)
        print(f"{self.name} says: {content}")
        self.add_memory(f"Talked with {other_agent.name}.")
        other_agent.add_memory(f"Talked with {self.name}.")


    def add_memory(self, memory):
        self.memories.append(memory)

    def search_memory(self, query):
        keywords = query.lower().split()
        relevant_memories = []

        for memory in self.memories:
            if any(keyword in memory.lower() for keyword in keywords):
                relevant_memories.append(memory)

        return relevant_memories

    def greet(self, other_agent):
        prompt = f"{self.name} greets {other_agent.name}. How does {other_agent.name} respond?"
        response = self.generate_response(prompt)
        print(f"{other_agent.name} responds: {response}")
        self.add_memory(f"Greeted {other_agent.name}.")
        other_agent.add_memory(f"Was greeted by {self.name} and responded with: {response}")


    def perform_action(self, action):
        self.current_action = action
        # Add code to execute the action or update the agent's state

    def add_task(self, task, time):
        self.tasks.append({"description": task, "time": time})

    def perform_tasks(self, current_time):
        tasks_to_perform = [task for task in self.tasks if task["time"] == current_time]
        for task in tasks_to_perform:
            print(f"{self.name} {task['description']}")
            self.tasks.remove(task)
            self.add_memory(f"I {task['description']}")

    def form_relationship(self, other_agent, initial_strength=0):
        self.relationships[other_agent.name] = initial_strength
        other_agent.relationships[self.name] = initial_strength

    def update_relationship(self, other_agent, change):
        self.relationships[other_agent.name] += change
        other_agent.relationships[self.name] += change

    def decide_on_task(self):
        # Implement logic to make decisions based on experiences and relationships.
        # For simplicity, you can randomly choose a task for now.
        import random
        if self.tasks:
            return random.choice(self.tasks)
        return None

    def generate_response(self, prompt):
        # Construct a context string based on the agent's memories
        context = f"{self.name} is a person with the following memories: {', '.join(self.memories)}."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
        )

        generated_response = response['choices'][0]['message']['content']
        return generated_response.strip()

    def __str__(self):
        return f"Agent {self.name}"
