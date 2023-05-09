def get_building(buildings, building_name):
    return buildings[building_name]

def get_room(buildings, room_name, building_name):
    return buildings[building_name].rooms[room_name]

def get_object(buildings, object_name, room_name, building_name):
    return buildings[building_name].rooms[room_name].objects[object_name]
