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