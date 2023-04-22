from agent import Agent


def main():
    agent = Agent(
        "Alice",
    )

    while True:
        command = input("Enter command (step): ")
        if command == "quit":
            break
        elif command == "step":
            print("Stepping...")
        else:
            print("Invalid agent name. Try again.")


if __name__ == "__main__":
    main()
