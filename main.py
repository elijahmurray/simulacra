from agent.agent import Agent
from world_clock import WorldClock
from config import NUMBER_OF_TIMES_TO_ADVANCE_WORLD
from shared_agent import agent
import requests


def main():
    world_clock = WorldClock()
    agents = [agent]

    for i in range(NUMBER_OF_TIMES_TO_ADVANCE_WORLD):
        world_clock.advance_time(agents)
        agent_dict = agent.to_dict()
        response = requests.post("http://127.0.0.1:5001/update_agent", json=agent_dict)
        if response.status_code != 200:
            print("Error updating agent in the server")


if __name__ == "__main__":
    main()
