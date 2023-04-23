from agent.agent import Agent
from world_clock import WorldClock

from config import NUMBER_OF_TIMES_TO_ADVANCE_WORLD

from seed_data import (
    agent_seed_data_gorgio,
    quick_start_data_gorgio,
    agent_seed_data_student,
    quick_start_data_student,
)


def main():
    # agent = Agent(
    #     "John Lin",
    # )
    agent = Agent(agent_seed_data_student, quick_start_data_student)

    world_clock = WorldClock()

    agents = [agent]

    # Sample time advancement
    for i in range(NUMBER_OF_TIMES_TO_ADVANCE_WORLD):
        world_clock.advance_time(agents)


if __name__ == "__main__":
    main()
