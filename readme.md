# Simulacra

Simulacra is a simulation of two agents interacting with each other. The agents have personalities, memories, tasks to perform, and can communicate with each other using natural language.

## Requirements

Simulacra requires the following dependencies:

- Python 3.7 or higher
- OpenAI API key (for natural language processing)
- `openai` Python package

## Setup

Create a virtual environment:
`python -m venv venv`

## Usage

To run Simulacra, simply execute the `main.py` file:

Start the venv:
`source venv/bin/activate`

Start the app:
`python3 main.py`

You will be presented with a command prompt where you can enter different commands to interact with the agents. The available commands are:

- `talk`: Simulate a conversation between two agents.
- `add_task`: Add a task for an agent to perform at a certain time.
- `perform_tasks`: Perform all tasks scheduled for an agent at the current time.
- `recall`: Search an agent's memories for specific keywords.
- `step`: Move the simulation forward by one time step.
- `quit`: Exit the simulation.

## Configuration
