from agent import Agent
from world_operations import create_world
import time

def game_loop(agents):
    while True:
        for agent in agents:
            reflection = agent.create_reflection()
            print(f"{agent.name} REFLECTS: {reflection}")
            plan = agent.create_plan()
            print(f"{agent.name} PLANS: {plan}")
            time.sleep(1)  # Adjust the sleep duration as needed
