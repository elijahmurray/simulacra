from scheduler import Scheduler
from agent import Agent

def main():
    alice = Agent("Alice")
    bob = Agent("Bob")

    agents = {"alice": alice, "bob": bob}

    alice.form_relationship(bob)

    alice.add_task("Go to the grocery store", 1)
    bob.add_task("Go to the park", 2)

    scheduler = Scheduler([alice, bob])

    while True:
        command = input("Enter command (greet, recall, add_task, perform_tasks, step, or quit): ")
        if command == "quit":
            break
        elif command == "step":
            scheduler.step()  # Add this line
        elif command in {"greet", "recall", "add_task", "perform_tasks"}:
            agent_name = input("Which agent? (alice or bob): ").lower()
            if agent_name in agents:
                if command == "greet":
                    other_agent_name = "bob" if agent_name == "alice" else "alice"
                    agents[agent_name].greet(agents[other_agent_name])
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
