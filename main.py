from scheduler import Scheduler
from agent import Agent

def main():
    agents = {"alice": Agent("Alice"), "bob": Agent("Bob")}
    scheduler = Scheduler()  # Add this line

    while True:
        command = input("Enter command (greet, recall, add_task, perform_task, step, or quit): ")
        if command == "quit":
            break
        elif command == "step":
            scheduler.step(agents)  # Add this line
        elif command in {"greet", "recall", "add_task", "perform_task"}:
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
                elif command == "perform_task":
                    agents[agent_name].perform_task()
            else:
                print("Invalid agent name. Try again.")
        else:
            print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
