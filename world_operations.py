from world_elements import Building, Room, Object

def create_world() -> dict:
    world = {}
    building1 = Building("Red House", [
        Room("Living Room", [Object("Sofa"), Object("TV")]),
        Room("Kitchen", [Object("Fridge"), Object("Stove")]),
    ])
    building2 = Building("Blue House", [
        Room("Living Room", [Object("Sofa"), Object("TV")]),
        Room("Kitchen", [Object("Fridge"), Object("Stove")]),
    ])

    world["buildings"] = [building1, building2]
    return world

def world_to_natural_language(element):
    # Convert the world element to natural language
    if isinstance(element, Building):
        rooms = ', '.join([room.name for room in element.rooms])
        return f"{element.name} contains the following rooms: {rooms}"
    elif isinstance(element, Room):
        objects = ', '.join([obj.name for obj in element.objects])
        return f"{element.name} contains the following objects: {objects}"
    elif isinstance(element, Object):
        return f"{element.name} is an object."
    else:
        return "Unknown element."

def find_elements_of_type(element, element_type: str) -> list:
    # Find all elements of the specified type within the element
    result = []
    if isinstance(element, Building):
        if element_type == "Room":
            result.extend(element.rooms)
        else:
            for room in element.rooms:
                result.extend(find_elements_of_type(room, element_type))
    elif isinstance(element, Room) and element_type == "Object":
        result.extend(element.objects)
    return result
