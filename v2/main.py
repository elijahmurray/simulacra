from agent import Agent
from world_clock import WorldClock


def main():
    agent = Agent(
        "Alice",
    )

    agents = [agent]

    world_clock = WorldClock()

    while True:
        command = input("Enter command (step): ")
        if command == "quit":
            break
        elif command == "step":
            world_clock.advance_time(agents)
        else:
            print("Invalid agent name. Try again.")


if __name__ == "__main__":
    main()
