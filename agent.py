import openai
import random


class Agent:
    def __init__(self, name, personality=None, background=None):
        self.name = name
        self.memories = []
        self.personality = (
            personality if personality else {"friendliness": 0.5, "formality": 0.5}
        )
        self.current_action = None
        self.tasks = []
        self.experiences = []
        self.relationships = {}
        self.add_memory(f"My name is {name}")
        self.background = (
            background
            if background
            else "This is the default background for me, {self.name}."
        )
        self.conversation_length = 0
        self.goodbye_triggers = [
            "bye",
            "goodbye",
            "talk to you later",
            "see you later",
            "take care",
        ]

        # Add the agent's background to their memories
        self.add_memory(
            f"{self.name}'s friendliness out of 1.0 is {self.personality['friendliness']} and formality out of 1.0 is {self.personality['formality']}."
        )
        self.add_memory(self.background)

    def generate_response(self, prompt):
        # Construct a context string based on the agent's memories
        context = f"{self.name} is a person with the following memories: {', '.join(self.memories)}."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system", "content": context},
                # {"role": "user", "content": "Seed: {random.randint(0, 100)}\n{prompt}"},
                {"role": "user", "content": prompt},
            ],
        )

        generated_response = response["choices"][0]["message"]["content"]
        return generated_response.strip()

    def generate_response_for_speaker(self, speaker, listener, prompt):
        content = self.generate_response(prompt)
        if content is None:
            return None
        print(f"{speaker.name} says: {content}")
        return content

    def generate_response_for_listener(self, speaker, listener):
        prompt = f"{speaker.name} says:"
        content = listener.generate_response(prompt)
        if content is None:
            return None
        print(f"{listener.name} says: {content}")
        listener.add_memory(f"Heard {speaker.name} say: {content}")
        return content

    def should_end_conversation(self, speaker, content):
        if any(trigger in content.lower() for trigger in speaker.goodbye_triggers):
            return True
        if speaker.conversation_length > 3:
            end_prob = 0.5
        elif speaker.conversation_length > 5:
            end_prob = 0.8
        elif speaker.conversation_length > 7:
            end_prob = 1.0
        else:
            end_prob = 0.0
        if (
            "boring" in content.lower()
            or "pointless" in content.lower()
            or "enough" in content.lower()
        ):
            end_prob += 0.2
        elif "interesting" in content.lower() or "fascinating" in content.lower():
            end_prob -= 0.2
        return random.random() < end_prob

    def talk(self, other_agent):
        agents = [self, other_agent]
        content = None
        conversation_ended = False
        while not conversation_ended:
            for i in range(2):
                speaker = agents[i]
                listener = agents[(i + 1) % 2]

                if content is not None:
                    prompt = (
                        f"{listener.name} said: {content}\n{speaker.name} responds:"
                    )
                    content = self.generate_response_for_speaker(
                        speaker, listener, prompt
                    )
                    if content is None:
                        continue
                else:
                    content = self.generate_response_for_listener(speaker, listener)

                conversation_ended = self.should_end_conversation(speaker, content)
                if conversation_ended:
                    # Have the speaker say goodbye
                    prompt = f"{listener.name} said: {content}\n{self.name} says:"
                    self.generate_response_for_speaker(speaker, listener, prompt)
                    break

                speaker.conversation_length += 1

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
        other_agent.add_memory(
            f"Was greeted by {self.name} and responded with: {response}"
        )

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

    def __str__(self):
        return f"Agent {self.name}"
