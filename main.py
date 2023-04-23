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
  while sim_clock==0:
    for _,agent in agents.items():
      agent.observe()
      sleep(1)
    state = environment.to_dict()
    state["sim_clock"] = sim_clock
    print(state)
    environment.save_state(state)
    sim_clock += SIM_CLOCK_INCREMENT

if __name__ == '__main__':
  main()
