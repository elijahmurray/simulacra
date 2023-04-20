class WorldElement:
    def __init__(self, name: str, element_type: str):
        self.name = name
        self.element_type = element_type

    def __repr__(self):
        return f"{self.element_type}: {self.name}"


class Building(WorldElement):
    def __init__(self, name: str, rooms=None):
        super().__init__(name, "Building")
        if rooms is None:
            rooms = []
        self.rooms = rooms


class Room(WorldElement):
    def __init__(self, name: str, objects=None):
        super().__init__(name, "Room")
        if objects is None:
            objects = []
        self.objects = objects


class Object(WorldElement):
    def __init__(self, name: str):
        super().__init__(name, "Object")


class AgentElement(WorldElement):
    def __init__(self, agent):
        super().__init__(agent.name, "Agent")
        self.agent = agent
