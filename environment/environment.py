from __future__ import annotations
import json
import pickle
from agent.agent import Agent
from environment.environment_objects import Building, Room, RoomObject
from environment.environment_utils import get_room
import datetime

class Environment:
    def __init__(self, sim_time: datetime.datetime, world_file_path: str = 'seed_data/world.json', agent_file_path: str = 'seed_data/agents.json') -> None:
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

        self.buildings = {}
        for bldg_json in world_data["buildings"]:
            bldg = Building(bldg_json["name"], bldg_json["type"])
            for room_json in bldg_json["rooms"]:
                room = Room(room_json["name"], bldg)
                for obj_json in room_json["objects"]:
                    obj = RoomObject(obj_json["name"], obj_json["type"], obj_json["state"], room)
                    room.add_object(obj)
                room.occupants = room_json["occupants"]
                bldg.add_room(room)
            self.buildings[bldg.name] = bldg
