import openai
from typing import Tuple, List, Dict
from config import API_KEY

openai.api_key = API_KEY

def generate_text(messages: List[Dict[str, str]], max_tokens: int = 200) -> str:

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.5,
        stop=None
    )

    return response.choices[0].message['content'].strip()

def ask_question(question: str, text: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text},
        {"role": "user", "content": question},
    ]
    return generate_text(messages, max_tokens=100)

# Add other functions for interacting with the language model
