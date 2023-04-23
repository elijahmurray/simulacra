class RoomObject:
    def __init__(self, name, obj_type, state, room):
        self.name = name
        self.type = obj_type
        self.state = state
        self.room = room

class Room:
    def __init__(self, name, building):
        self.name = name
        self.objects = {}
        self.occupants = []
        self.building = building

    def add_object(self, obj):
        self.objects[obj.name] = obj

    def remove_object(self, obj):
        del self.objects[obj.name]

    def add_occupant(self, occupant):
        self.occupants.append(occupant)

    def remove_occupant(self, occupant):
        self.occupants.remove(occupant)

class Building:
    def __init__(self, name, bldg_type):
        self.name = name
        self.type = bldg_type
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.name] = room

def process_object(obj):
        return f"The {obj.name} in the {obj.room.name} in {obj.room.building.name} is {obj.state}."

def process_room(room):
    observations = []
    if len(room.occupants) > 0:
        occupants = ", ".join(room.occupants)
        observations.append(f"The occupants of the {room.name} are {occupants}.")
    for obj in room.objects.values():
        observations.append(process_object(obj))
    return observations

def process_building(building):
    observations = []
    for room in building.rooms.values():
        observations.extend(process_room(room))
    return observations

def process_world():
    observations = []
    for building in buildings.values():
        observations.extend(process_building(building))
