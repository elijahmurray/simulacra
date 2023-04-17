import openai
from scheduler import Scheduler
from agent import Agent

openai.api_key = "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"


def main():
    alice_personality = {"friendliness": 0.2, "formality": 0.2}
    bob_personality = {"friendliness": 0.2, "formality": 0.3}

    alice = Agent(
        "Alice",
        personality=alice_personality,
        background="Alice is a software engineer who loves hiking and playing video games in her free time.",
    )
    bob = Agent(
        "Bob",
        personality=bob_personality,
        background="Bob is a sales executive with 10 years of experience in the technology industry. He is known for his outgoing personality and exceptional communication skills. In his free time, Bob enjoys playing basketball and volunteering at his local animal shelter. He is married with two children and enjoys spending time with his family.",
    )

    agents = {"alice": alice, "bob": bob}

    alice.form_relationship(bob)

    alice.add_task("Go to the grocery store", 1)
    bob.add_task("Go to the park", 2)

    scheduler = Scheduler([alice, bob])

    # num_conversations = 1  # Change this to the number of conversations you want
    # for _ in range(num_conversations):
    # agents["alice"].talk(agents["bob"])

    while True:
        command = input(
            "Enter command (talk, recall, add_task, perform_tasks, step, or quit): "
        )
        if command == "quit":
            break
        elif command == "step":
            scheduler.step()  # Add this line
        elif command in {"talk", "recall", "add_task", "perform_tasks"}:
            agent_name = input("Which agent? (alice or bob): ").lower()
            if agent_name in agents:
                if command == "talk":
                    if agent_name in agents:
                        other_agent_name = "bob" if agent_name == "alice" else "alice"
                        agents[agent_name].talk(agents[other_agent_name])
                elif command == "recall":
                    # Below commented code is for searching memories
                    # query = input("Enter a search query: ")
                    # memories = agents[agent_name].search_memory(query)
                    # print(f"{agent_name.capitalize()}'s memories related to '{query}':")
                    memories = agents[agent_name].memories
                    print(f"{agent_name.capitalize()}'s memories:")
                    for memory in memories:
                        print("-", memory)
                elif command == "add_task":
                    task = input("Enter a task description: ")
                    time = int(input("Enter the scheduled time for the task: "))
                    agents[agent_name].add_task(task, time)  # Add the time parameter
                elif command == "perform_tasks":
                    agents[agent_name].perform_tasks(
                        scheduler.time
                    )  # Pass the current time
            else:
                print("Invalid agent name. Try again.")
        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
