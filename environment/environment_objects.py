from __future__ import annotations
from typing import List

class RoomObject:
    """A class representing an object within a room."""

    def __init__(self, name: str, obj_type: str, state: str, room: Room) -> None:
        """
        Initialize a RoomObject instance.

        :param name: The name of the object.
        :param obj_type: The type of the object.
        :param state: The current state of the object.
        :param room: The room in which the object is located.
        """
        self.name, self.type, self.state, self.room = name, obj_type, state, room


class Room:
    """A class representing a room within a building."""

    def __init__(self, name: str, building: Building) -> None:
        """
        Initialize a Room instance.

        :param name: The name of the room.
        :param building: The building in which the room is located.
        """
        self.name, self.building, self.objects, self.occupants = name, building, {}, []

    def __str__(self) -> str:
        return f"{self.name} in {self.building.name}"

    def add_object(self, obj: RoomObject) -> None:
        """
        Add a RoomObject to the room.

        :param obj: The RoomObject instance to add.
        """
        self.objects[obj.name] = obj

    def remove_object(self, obj: RoomObject) -> None:
        """
        Remove a RoomObject from the room.

        :param obj: The RoomObject instance to remove.
        """
        del self.objects[obj.name]

    def add_occupant(self, occupant: str) -> None:
        """
        Add an occupant to the room.

        :param occupant: The name of the occupant.
        """
        self.occupants.append(occupant)

    def remove_occupant(self, occupant: str) -> None:
        """
        Remove an occupant from the room.

        :param occupant: The name of the occupant.
        """
        self.occupants.remove(occupant)


class Building:
    """A class representing a building containing rooms."""

    def __init__(self, name: str, bldg_type: str) -> None:
        """
        Initialize a Building instance.

        :param name: The name of the building.
        :param bldg_type: The type of the building.
        """
        self.name, self.type, self.rooms = name, bldg_type, {}

    def __str__(self) -> str:
        return f"{self.name}"

    def add_room(self, room: Room) -> None:
        """
        Add a Room instance to the building.

        :param room: The Room instance to add.
        """
        self.rooms[room.name] = room


def process_object(obj: RoomObject) -> str:
    """
    Process a RoomObject instance and return a formatted string.

    :param obj: The RoomObject instance to process.
    :return: A formatted string describing the object's state and location.
    """
    return f"The {obj.name} in the {obj.room.name} in {obj.room.building.name} is {obj.state}."


def process_room(room: Room) -> List[str]:
    """
    Process a Room instance and return a formatted string of the state and location of all RoomObjects and occupants within the room.

    :param room: The Room instance to process.
    :return: A formatted string of the state and location of all RoomObjects and occupants within the room.
    """
    occupants_str = (
        f"The occupants of the {room.name} are {', '.join(room.occupants)}."
        if room.occupants
        else ""
    )
    object_strs = [process_object(obj) for obj in room.objects.values()]

    return [s for s in [occupants_str] + object_strs if s]


def process_building(building: Building) -> List[str]:
    """
    Process a Building instance and return a formatted string of the state and location of all RoomObjects within all rooms in the building.

    :param obj: The Building instance to process.
    :return: A formatted string of the state and location of all RoomObjects and occupants within all Rooms in the Building.
    """
    return [observation for room in building.rooms.values() for observation in process_room(room)]
