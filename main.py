import json
from environment import Environment
from agent import Agent
from config import SIM_CLOCK_INCREMENT
from time import sleep

def main():

  # INSTANTIATE ENVIRONMENT AND AGENTS STATE
  environment = Environment()
  agents = environment.agents
  print(agents)

  # START SIMULATION
  sim_clock = 0
  while True:
    for _,agent in agents.items():
      agent.observe()
      for memory in agent.memory_stream:
        print(memory.description)
      sleep(10)
    sim_clock += SIM_CLOCK_INCREMENT

if __name__ == '__main__':
  main()
