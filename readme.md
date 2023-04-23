# Agent Simulator

This project is inpired by the [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) paper from Stanford and Google. The goal is to recreate interaction between GPT powered agents, that can freely plan their days, interact, and reflect based on their interactions with the world and their memories.

Current status: Based on seed data, an agent can currently plan and execute their day based on their simplified memories and daily plan. Please see the [stable branch](https://github.com/elijahmurray/simulacra/tree/stable) if you're interested in experimenting.

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

Edit your config variables in `config.py`:

- Set `TIME_INTERVAL` to however many minutes of in-game time should pass per step
- Set `NUMBER_OF_TIMES_TO_ADVANCE_WORLD`

## Usage / Run
Run the main script.

`python main.py`


## Debugging
To have more robust debugging, you can turn on various levels of logging using the variables found in the `config.py`, which determines system logging in the `handle_logging` method in `helpers.py`.

## License
This project is licensed under the MIT License.