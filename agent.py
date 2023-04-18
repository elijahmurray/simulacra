import openai
import random


class Agent:
    def __init__(self, name, personality=None, background=None):
        self.name = name
        self.personality = (
            personality if personality else {"friendliness": 0.5, "formality": 0.5}
        )
        self.current_action = None
        self.tasks = []
        self.relationships = {}
        self.short_term_memory = []
        self.long_term_memory = []
        self.conversation_length = 0
        self.goodbye_triggers = [
            "bye",
            "goodbye",
            "talk to you later",
            "see you later",
            "take care",
        ]

        self.background = (
            background
            if background
            else f"This is the default background for me, {self.name}."
        )

        # Add the agent's background to their long-term memory
        self.add_to_long_term_memory(self.background)

    def add_to_short_term_memory(self, memory):
        self.short_term_memory.append(memory)

    def add_to_long_term_memory(self, memory):
        self.long_term_memory.append(memory)

    def transfer_to_long_term_memory(self):
        self.long_term_memory.extend(self.short_term_memory)
        self.short_term_memory = []

    def reflect(self):
        self.transfer_to_long_term_memory()

    def plan(self):
        task = self.decide_on_task()
        if task:
            self.perform_action(task["description"])

    def step(self):
        self.reflect()

        action = random.choice(
            ["add_task", "perform_task", "interact", "form_relationship"]
        )

        if action == "add_task":
            self.autonomous_add_task()
        elif action == "perform_task":
            self.perform_tasks(self.scheduler.time)
        elif action == "interact":
            other_agent = random.choice(self.scheduler.agents)
            if other_agent != self:
                self.talk(other_agent)
        elif action == "form_relationship":
            other_agent = random.choice(self.scheduler.agents)
            if other_agent != self and other_agent.name not in self.relationships:
                self.form_relationship(other_agent)

    def autonomous_add_task(self):
        task_pool = [
            "make breakfast",
            "go for a walk",
            "clean the room",
            "work out",
            "read a book",
            "call a friend",
            "watch TV",
            "go shopping",
        ]
        task = random.choice(task_pool)
        time = self.scheduler.time + random.randint(1, 5)
        self.add_task(task, time)

    def generate_response(self, prompt):
        context = f"{self.name} is a person with the following memories: {', '.join(self.long_term_memory)}."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ],
        )

        generated_response = response["choices"][0]["message"]["content"]
        return generated_response.strip()

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
                    content = speaker.generate_response(prompt)
                    if content is None:
                        continue
                else:
                    prompt = (
                        f"{speaker.name} starts a conversation with {listener.name}:"
                    )
                    content = speaker.generate_response(prompt)

                print(f"{speaker.name} says: {content}")
                listener.add_to_short_term_memory(
                    f"Heard {speaker.name} say: {content}"
                )

                conversation_ended = speaker.should_end_conversation(content)
                if conversation_ended:
                    break

                speaker.conversation_length += 1

    def should_end_conversation(self, content):
        if any(trigger in content.lower() for trigger in self.goodbye_triggers):
            return True
        if self.conversation_length > 3:
            end_prob = 0.5
        elif self.conversation_length > 5:
            end_prob = 0.8
        elif self.conversation_length > 7:
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
            self.add_to_long_term_memory(f"I {task['description']}")

    def form_relationship(self, other_agent, initial_strength=0):
        self.relationships[other_agent.name] = initial_strength
        other_agent.relationships[self.name] = initial_strength

    def update_relationship(self, other_agent, change):
        self.relationships[other_agent.name] += change
        other_agent.relationships[self.name] += change

    def decide_on_task(self):
        if self.tasks:
            return random.choice(self.tasks)
        return None

    def __str__(self):
        return f"Agent {self.name}"
