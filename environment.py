import json
from agent import Agent
from typing import List
from environment_objects import Building, Room, RoomObject
import datetime

class Environment:
    def __init__(self, sim_time: datetime.datetime, world_file_path: str = 'init_data/world_config.json', agent_file_path: str = 'init_data/agent_config.json'):
        """
        Creates the environment with the buildings, rooms, objects, and agents.
        """
        print("loading world and agent data")
        with open(world_file_path) as f:
            world_data = json.load(f)["world"]
        with open(agent_file_path) as f:
            agent_data = json.load(f)["agents"]
        print("creating world")
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
        print("creating agents")
        self.agents = {}
        for agent_json in agent_data:
            starting_location = self.get_room(agent_json["starting_location"]["room_name"], agent_json["starting_location"]["building_name"])
            # Create the agent
            agent = Agent(
                name = agent_json["name"],
                age = agent_json["age"],
                description=agent_json["description"],
                starting_location=starting_location,
                sim_time=sim_time
            )
            self.agents[agent.name] = agent
            # Add the agent as an occupant of the starting location, and update the locations cache
            starting_location.add_occupant(agent.name)

    def to_dict(self):
        """
        Converts the environment state to a dictionary.
        """
        state = {
            "buildings": {},
            "agents": {}
        }

        # Add building state
        for building_name, building in self.buildings.items():
            state["buildings"][building_name] = {
                "type": building.type,
                "rooms": {}
            }
            for room_name, room in building.rooms.items():
                state["buildings"][building_name]["rooms"][room_name] = {
                    "objects": {},
                    "occupants": room.occupants
                }
                for obj_name, obj in room.objects.items():
                    state["buildings"][building_name]["rooms"][room_name]["objects"][obj_name] = {
                        "type": obj.type,
                        "state": obj.state
                    }

        # Add agent state
        for agent_name, agent in self.agents.items():
            state["agents"][agent_name] = {
                "age": agent.age,
                "description": agent.description,
                "current_day_plan": agent.current_day_plan,
                "current_block_plan": agent.current_block_plan,
                #"current_activity": agent.current_activity,
                #"current_observations": agent.current_observations,
                "location": {
                    "building": agent.location.building.name,
                    "room": agent.location.name
                },
            }

        return state

    def save_state(self, state, file_path: str = 'server_data/state.json'):
        """
        Saves the environment state to a JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(state, f, indent=2)

    def get_all_buildings(self):
        return self.buildings.keys()

    def get_all_rooms(self):
        rooms = []
        buildings = self.get_all_buildings()
        for building in buildings:
            for room in self.buildings[building].rooms.keys():
                rooms.append(f"{room} in {building}")
        return rooms

    # UNSURE IF BELOW FUNCTIONS ARE NEEDED, MARK FOR REVIEW
    def get_building(self, building_name):
        return self.buildings[building_name]

    def get_room(self, room_name, building_name):
        return self.buildings[building_name].rooms[room_name]

    def get_object(self, object_name, room_name, building_name):
        return self.buildings[building_name].rooms[room_name].objects[object_name]
