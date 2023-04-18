# Agent Simulation

This project simulates a basic interaction between two agents, Alice and Bob, using the OpenAI API. The agents can have conversations, perform tasks, and form relationships. The simulation uses a scheduler to keep track of time and manage the agents' actions.

Inspired by the Stanford x Google experiment in generative agent human simulating interactions.

Very much a WIP currently. See roadmap below.

## Setup

1. Install Python 3.7 or higher.

2. Clone the repository.
`git clone https://github.com/yourusername/yourrepository.git`

3. Change the directory.
`cd yourrepository`

4. Set up a virtual environment.
`python3 -m venv venv`

5. Activate the virtual environment.
```
source venv/bin/activate # For Linux and macOS
venv\Scripts\activate # For Windows
```

6. Install the required packages.
`pip install -r requirements.txt`

7. Setup your openAI key
`cp .env.template .env`

Edit the `.env` file to put in your OpenAI private key


## Configuration

1. Create an OpenAI account and obtain your API key.

2. Replace the placeholder API key in `main.py` with your own API key.
```python
openai.api_key = "your-api-key"
```

## Usage
Run the main script.

`python main.py`

Follow the on-screen instructions to interact with the agents. You can issue the following commands:

- talk: Make the agents have a conversation.
- recall: Display an agent's long-term memories.
- add_task: Add a task for an agent to perform.
- perform_tasks: (Deprecated) Tasks are now performed automatically during the step command.
- step: Move the simulation forward by one time unit.
- quit: Exit the simulation.

## Files
- main.py: The main script that runs the simulation.
- agent.py: Contains the Agent class definition, which represents an individual agent.
- scheduler.py: Contains the Scheduler class definition, which manages the agents' actions over time.

## Roadmap

- [x] Agent
- [x] Global time
- [x] Dialogue
- [x] Task management
- [x] Task extraction from dialogue
- [x] more realistic dialogue
- [x] OpenAI setup + dialogue
- [x] Simple memory system (long term + short term)
- [ ] Daily planning
- [ ] Goal setting, objectives, and long term planning
- [ ] Robust long term and short term memory truncating
- [ ] God mode
- [ ] Environment interaction
- [ ] More personality, traits, and emotions
- [ ] Suggestions?

## License
This project is licensed under the MIT License.

