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

# To run
To run: `cd v2 && python main.py` or `python v2/main.py`

# Debugging
To have more robust debugging, you can turn on various levels of logging using the variables found in the `handle_logging` method.