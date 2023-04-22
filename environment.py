import json

class Environment:
    def __init__(self, config_path: str = 'init_data/environment_config.json'):
        with open(config_path, 'r') as f:
            self.world = json.load(f)["world"]

def get_location_by_name(world, location_name, location_type):
    if location_type == "room":
        for building in world["buildings"]:
            for room in building["rooms"]:
                if room["name"] == location_name:
                    return room
    elif location_type == "building":
        for building in world["buildings"]:
            if building["name"] == location_name:
                return building
    return None

def process_object(object):
    return f"The {object['name']} is {object['state']}."

def process_room_objects(room):
    observations = []
    if "objects" in room:
        for item in room["objects"]:
            observations.append(process_object(item))
    return observations

def process_room(room, location):
    observations = []
    if "objects" in room:
        for item in room["objects"]:
            observations.append(f"There is a {item['name']} in the {location}.")
    return observations

def process_building(building):
    if "rooms" in building:
        observations = []
        for room in building["rooms"]:
            observations.extend(process_room(room, f"{room['name']} at {building['name']}"))
    return observations

def process_world(world):
    if "buildings" in world:
        observations = []
        for building in world["buildings"]:
           observations.extend(process_building(building))
    return observations
