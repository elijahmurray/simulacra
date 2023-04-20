import json

def load_config(filename: str) -> dict:
    with open(filename, 'r') as file:
        return json.load(file)

def save_config(filename: str, config: dict):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=2)
