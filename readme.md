# Generative Agent Simulation

## What is this?

This codebase is an implementation of [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442).

## How to run

From the root directory:

1. Install dependencies:

`pip install -r requirements.txt`

2. Create a .env file from the .env.template file and set `OPEN_AI_API_KEY` to your OpenAI API key.

3. Run the simulation

`python main.py`

## Repository Structure

- **Environment**: The area in which agents live, move around, and act. Includes a series of Buildings, which contain Rooms, which in turn contain RoomObjects that agents can interact with, like chairs and tables to sit down at, kitchen appliances, and devices like computers.
  - **environment_objects.py**: Classes representing environment objects including Buildings, Rooms, and Objects.
  - **environment.py**: Class for the simulation environment including the world and agents in the world.
  - **environment_utils.py**: Utils for the Environment class.
- **Agents**: The players in the game, powered by an LLM, that have beliefs and desires that result in intentions, and observe their surroundings and react to carry out actions consistent with their intentions.
  - **agent.py**: Class for the agents in the simulation.
  - **utils.py**: Utils for the agent class.
- **Memory**: Each agent has a Memory Stream, which holds Memory objects that represent an agent's memories and provides helper functions to access relevant memories, create reflections, and store the three different types of memories: observations, reflections, and dialogue.
  - **memory.py**: Dataclass representing the Memory object.
  - **memory_stream.py**: Class to manage an agent's memory stream including memory retrieval, reflection creation, etc. Must have an Agent parent.
  - **utils.py**:
- **Utils**: A catch-all component for any helper functions like logging, state management, wrappers for external infrastructure like vector databases and LLM APIs, and other miscellaneous tasks like formatting dates.
  - **logging.py**: Utils for logging output across the simulation.
  - **vector_db.py**: Classes to interact with different vector DBs like Pinecone and ChromaDB
  - **formatting.py**: Utils for dealing with data formatting like conversting dates to strings and back again.
  - **storage.py**: Utils for serializing and deserializing simulation state.
  - **llm.py**: Utils for interacting with LLMs like `gpt-3.5-turbo`.
- **Config**: All configuration objects like variables, prompts, etc.
  - **settings.py**: Various simulation settings.
  - **prompts.py**: Prompt templates used in LLM calls.
- **server.py**: A game server that exposes a REST API to inspect game state.
- **main.py**: main file.
