from agent import Agent
from world_operations import create_world
from game_loop import game_loop
from threading import Thread
from server import app

if __name__ == "__main__":
    world = create_world()

    # Initialize agents
    agents = [
        Agent("Agent1", "Agent1 is a curious explorer.", world),
        Agent("Agent2", "Agent2 is a cautious observer.", world)
    ]

    # Start the game loop in a separate thread
    game_loop_thread = Thread(target=game_loop, args=(agents,))
    game_loop_thread.start()

    # Start the Flask server
    app.run(port=3000)
