import openai
from scheduler import Scheduler
from agent import Agent

openai.api_key = "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"

def main():
    alice = Agent("Alice")
    bob = Agent("Bob")

    agents = {"alice": alice, "bob": bob}

    alice.form_relationship(bob)

    alice.add_task("Go to the grocery store", 1)
    bob.add_task("Go to the park", 2)

    scheduler = Scheduler([alice, bob])

    num_conversations = 3  # Change this to the number of conversations you want
    for _ in range(num_conversations):
        agents['alice'].talk(agents['bob'])

    while True:
        command = input("Enter command (talk, recall, add_task, perform_tasks, step, or quit): ")
        if command == "quit":
            break
        elif command == "step":
            scheduler.step()  # Add this line
        elif command in {"talk", "recall", "add_task", "perform_tasks"}:
            agent_name = input("Which agent? (alice or bob): ").lower()
            if agent_name in agents:
                if command == "talk":
                    agent_name = input("Which agent? (alice or bob): ").lower()
                    if agent_name in agents:
                        other_agent_name = "bob" if agent_name == "alice" else "alice"
                        agents[agent_name].talk(agents[other_agent_name])
                elif command == "recall":
                    query = input("Enter a search query: ")
                    memories = agents[agent_name].search_memory(query)
                    print(f"{agent_name.capitalize()}'s memories related to '{query}':")
                    for memory in memories:
                        print("-", memory)
                elif command == "add_task":
                    task = input("Enter a task description: ")
                    time = int(input("Enter the scheduled time for the task: "))
                    agents[agent_name].add_task(task, time)  # Add the time parameter
                elif command == "perform_tasks":
                    agents[agent_name].perform_tasks(scheduler.time)  # Pass the current time
            else:
                print("Invalid agent name. Try again.")
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
