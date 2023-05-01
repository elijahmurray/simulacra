from __future__ import annotations
import json
import pickle
from agent import Agent
from environment_objects import Building, Room, RoomObject
import datetime

class Environment:
    def __init__(self, sim_time: datetime.datetime, world_file_path: str = 'init_data/world_config.json', agent_file_path: str = 'init_data/agent_config.json') -> None:
        """
        Initialize the Environment instance with buildings, rooms, objects, and agents based on the provided configuration files.

        :param sim_time: The current simulation time as a datetime object.
        :param world_file_path: The path to the world configuration file. Defaults to 'init_data/world_config.json'.
        :param agent_file_path: The path to the agent configuration file. Defaults to 'init_data/agent_config.json'.
        """
        with open(world_file_path) as f:
            world_data = json.load(f)["world"]
        with open(agent_file_path) as f:
            agent_data = json.load(f)["agents"]

        self.buildings = {bldg["name"]: Building(bldg["name"], bldg["type"], {
            room["name"]: Room(room["name"], bldg["name"], {
                obj["name"]: RoomObject(obj["name"], obj["type"], obj["state"], room["name"], bldg["name"]) for obj in room["objects"]
            }, room["occupants"]) for room in bldg["rooms"]
        }) for bldg in world_data["buildings"]}

        self.agents = {agent["name"]: Agent(agent["name"], agent["age"], agent["description"], self.get_room(agent["starting_location"]["room_name"], agent["starting_location"]["building_name"]), sim_time) for agent in agent_data}
