import pickle

def get_building(buildings, building_name):
    return buildings[building_name]

def get_room(buildings, room_name, building_name):
    return buildings[building_name].rooms[room_name]

def get_object(buildings, object_name, room_name, building_name):
    return buildings[building_name].rooms[room_name].objects[object_name]

def read_pickle(file_path: str = 'cached_data/environment.pkl') -> object:
    with open(file_path, 'rb') as f:
        return pickle.load(f)
