from agent.agent import Agent
from world_clock import WorldClock

from prompts import (
    agent_seed_data_gorgio,
)


def main():
    # agent = Agent(
    #     "John Lin",
    # )
    agent = Agent(agent_seed_data_gorgio)

    world_clock = WorldClock()

    agents = [agent]

    # Sample time advancement
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)
    world_clock.advance_time(agents)


if __name__ == "__main__":
    main()
