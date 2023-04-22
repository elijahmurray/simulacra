import json
from environment import Environment
from agent import Agent
from config import SIM_CLOCK_INCREMENT
from copy import deepcopy

def main():

  # INSTANTIATE ENVIRONMENT
  enviornment = Environment()
  world = enviornment.world

  # INSTANTIATE AGENTS
  agents = []
  with open('init_data/agent_config.json') as f:
    agent_config = json.load(f)
  for agent in agent_config['agents']:
    agents.append(Agent(agent, world))

  # INSTANTIATE SIMULATION STATE
  state = deepcopy(world)
  for agent in agents:
    location_path = agent.location.split(":")
    print(state["buildings"][location_path[0]][location_path[1]])
    state["buildings"][location_path[0]][location_path[1]]['occupants'] = []
    state["buildings"][location_path[0]][location_path[1]]['occupants'].append(agent.name)
  json.dump(state, open('server_data/environment_state.json', 'w'))

  # START SIMULATION
  sim_clock = 0
  while True:
    for agent in agents:
      print(agent.name, agent.location)
      #agent.observe(world, agent.location)
      #agent.plan()
      #agent.react()
    sim_clock += SIM_CLOCK_INCREMENT

if __name__ == '__main__':
  main()
