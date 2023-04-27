import json
from environment import Environment
from agent import Agent
from config import SIM_CLOCK_INCREMENT_MINUTES
from time import sleep
import datetime
from utils import save_pickle_environment

def main():


  sim_time = datetime.datetime(2023, 2, 1, 10, 0)

  print(f"Starting simulation at {sim_time}")
  # INSTANTIATE ENVIRONMENT AND AGENTS STATE
  environment = Environment(sim_time)
  print("Environment instantiated")
  agents = environment.agents
  print("Agents instantiated")
  # START SIMULATION CLOCK
  # Artificial counter for dev
  count = 0

  while True:
    for _,agent in agents.items():
      agent.sim_time = sim_time
      agent.environment = environment.buildings
      agent.process_game_step()
      print(f"Executed step at time {agent.sim_time} for {agent.name}")
      print(f"{agent.name}'s current location: {str(agent.location)}")
      print(f"{agent.name} has observed the following: {[str(observation) for observation in agent.current_observations]}")
      print(f"{agent.name}'s current day plan: {agent.current_day_plan}")
      print(f"{agent.name}'s current block plan: {agent.current_block_plan}")
      print(f"{agent.name}'s current activity: {agent.current_activity}")

    # Save state
    #state = environment.to_dict()
    #state["sim_time"] = sim_time.strftime("%Y-%m-%d %H:%M:%S")
    #environment.save_state(state)
    save_pickle_environment(environment)

    # Increment simulation clock
    sim_time += datetime.timedelta(minutes=SIM_CLOCK_INCREMENT_MINUTES)
    # Sleep to avoid rate limit
    sleep(10)
    # Counter increment for dev
    count += 1

if __name__ == '__main__':
  main()
