class Agent:
    def __init__(self, name):
        self.name = name
        self.memories = []
        self.current_action = None
        self.tasks = []
        self.add_memory(f"My name is {name}")


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
        print(f"{self.name} greets {other_agent.name}.")
        self.add_memory(f"Greeted {other_agent.name}.")
        other_agent.add_memory(f"Was greeted by {self.name}.")

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

    def __str__(self):
        return f"Agent {self.name}"
