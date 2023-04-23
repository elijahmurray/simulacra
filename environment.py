import json
from agent import Agent
from typing import List
from environment_objects import Building, Room, RoomObject

class Environment:
    def __init__(self, world_file_path: str = 'init_data/world_config.json', agent_file_path: str = 'init_data/agent_config.json'):
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

        # Initialize agents with starting location
        self.agents = {}
        for agent_json in agent_data:
            starting_location = self.get_room(agent_json["starting_location"]["room_name"], agent_json["starting_location"]["building_name"])
            # Create the agent
            agent = Agent(
                name = agent_json["name"],
                description=agent_json["description"],
                starting_location=starting_location)
            self.agents[agent.name] = agent
            # Add the agent as an occupant of the starting location, and update the locations cache
            starting_location.add_occupant(agent.name)

    def get_building(self, building_name):
        return self.buildings[building_name]

    def get_room(self, room_name, building_name):
        return self.buildings[building_name].rooms[room_name]

    def get_object(self, object_name, room_name, building_name):
        return self.buildings[building_name].rooms[room_name].objects[object_name]


