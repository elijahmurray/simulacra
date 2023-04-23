import openai
import random
import re
from datetime import timedelta


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
        self.steps = 0
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

        # Transfer short-term memories to long-term memory every 10 steps
        if self.steps % 10 == 0:
            self.transfer_to_long_term_memory()

        # Increment the steps attribute
        self.steps += 1

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
        time = self.scheduler.time + timedelta(minutes=random.randint(30, 150))
        self.add_task(task, time)

    def generate_response(self, prompt):
        # Limit memories to the last 10 items
        short_term_memories = ", ".join(self.short_term_memory[-10:])
        long_term_memories = ", ".join(self.long_term_memory[-10:])

        context = f"{self.name} is a person with the following short-term memories: {short_term_memories} and long-term memories: {long_term_memories}."

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
                    prompt = f"{speaker.name}, start a converation with {listener.name}, and see where the conversation leads you. You may want to talk about shared memories, make plans, deepen your relationship, or talk about anything you want to:"
                    content = speaker.generate_response(prompt)

                print("\n" + "-" * 40)
                print(f"{speaker.name} says: {content}")
                print("-" * 40 + "\n")
                listener.add_to_short_term_memory(
                    f"Heard {speaker.name} say: {content}"
                )
                # Extract and add tasks from conversation
                tasks = self.extract_tasks_from_conversation(content)
                for task in tasks:
                    scheduled_time = self.schedule_task(task)
                    self.add_task(task, scheduled_time)
                    other_agent.add_task(task, scheduled_time)
                    print(
                        f"Added task '{task}' for both agents at time {scheduled_time}"
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

    def extract_tasks_from_conversation(self, content):
        task_phrases = ["let's ", "we should ", "we can ", "how about we "]
        tasks = []

        for phrase in task_phrases:
            regex_pattern = re.escape(phrase) + r"([\w\s]+)"
            matches = re.findall(regex_pattern, content.lower())
            tasks.extend(matches)

        return tasks

    def schedule_task(self, task):
        current_time = self.scheduler.time
        # Round the current time to the nearest 30-minute mark
        minutes = (current_time.minute // 30) * 30
        rounded_time = current_time.replace(minute=minutes, second=0, microsecond=0)

        # Schedule the task for a random 30-minute interval in the next 24 hours
        time_slots = 2 * 24  # 2 slots per hour, for 24 hours
        future_slots = random.randint(1, time_slots)
        scheduled_time = rounded_time + timedelta(minutes=30 * future_slots)
        self.add_task(task, scheduled_time)
        return scheduled_time

    def perform_action(self, action):
        self.current_action = action
        # Add code to execute the action or update the agent's state

    def add_task(self, task, time, urgency=0.5, importance=0.5, preference=0.5):
        self.tasks.append(
            {
                "description": task,
                "time": time,
                "urgency": urgency,
                "importance": importance,
                "preference": preference,
            }
        )

    def decide_on_task(self):
        if self.tasks:
            # Calculate priority based on urgency, importance, and preference
            for task in self.tasks:
                task["priority"] = (
                    task["urgency"] + task["importance"] + task["preference"]
                )

            # Choose the task with the highest priority
            highest_priority_task = max(self.tasks, key=lambda x: x["priority"])
            return highest_priority_task
        return None

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
