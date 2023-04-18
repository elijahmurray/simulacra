import openai
from scheduler import Scheduler
from agent import Agent
import dotenv
import os


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
    alice_personality = {"friendliness": 0.2, "formality": 0.2}
    bob_personality = {"friendliness": 0.2, "formality": 0.3}

    agent1 = Agent(
        "Alice",
        personality=alice_personality,
        background="Meet Alice, a 25-year-old software developer from Chicago. Growing up in a family of engineers, Alice was always drawn to technology and coding. She earned her bachelor's degree in computer science from the University of Illinois and landed a job at a tech company in Silicon Valley. Alice is known for her problem-solving skills and attention to detail, which have earned her a reputation as a reliable and efficient developer. Outside of work, Alice enjoys hiking and exploring the outdoors, as well as reading science fiction novels. Her calm and composed demeanor helps her navigate through high-pressure situations both in her personal and professional life.",
    )
    agent2 = Agent(
        "Bob",
        personality=bob_personality,
        background="Bob is a sales executive with 10 years of experience in the technology industry. He is known for his outgoing personality and exceptional communication skills. In his free time, Bob enjoys playing basketball and volunteering at his local animal shelter. He is married with two children and enjoys spending time with his family.",
    )

    scheduler = Scheduler([agent1, agent2])

    # Set scheduler for both agents
    agent1.scheduler = scheduler
    agent2.scheduler = scheduler

    # Set the number of steps for the simulation
    num_steps = 100

    # Run the simulation for the specified number of steps
    for _ in range(num_steps):
        scheduler.step()

    agents = {"alice": agent1, "bob": agent2}

    while True:
        command = input(
            "Enter command (talk, recall, add_task, perform_tasks, step, or quit): "
        )
        if command == "quit":
            break
        elif command == "step":
            scheduler.step()
        elif command in {"talk", "recall", "add_task", "perform_tasks"}:
            agent_name = input("Which agent? (alice or bob): ").lower()
            if agent_name in agents:
                if command == "talk":
                    if agent_name in agents:
                        other_agent_name = "bob" if agent_name == "alice" else "alice"
                        agents[agent_name].talk(agents[other_agent_name])
                elif command == "recall":
                    memories = agents[agent_name].long_term_memory
                    print(f"{agent_name.capitalize()}'s memories:")
                    for memory in memories:
                        print("-", memory)
                elif command == "add_task":
                    task = input("Enter a task description: ")
                    time = int(input("Enter the scheduled time for the task: "))
                    agents[agent_name].add_task(task, time)
                elif command == "perform_tasks":
                    print(
                        "Tasks are now performed automatically during the step command."
                    )
            else:
                print("Invalid agent name. Try again.")
        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
