import openai
from config import OPENAI_MODEL, MAX_TOKENS
from dotenv import load_dotenv
import os
from time import sleep

# SET UP CLIENT
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_API_KEY")

def call_llm(prompt_template: str, data: dict, max_tokens: int = MAX_TOKENS, temperature: float = 0.2, max_retries: int = 2):
    '''
    Calls the LLM with a prompt and returns the response text.
    Requires that the data dictionary provided has keys that match the prompt's template variables, or error will be thrown.
    '''
    try:
        prompt = prompt_template.format(**data)
    except KeyError as e:
        raise Exception("The data dictionary provided is missing keys required by the prompt template. Please check the prompt template and the data dictionary provided.")
    retries = 0
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
            result = response['choices'][0]['message']['content']
            return result
        except openai.error.RateLimitError as e:
            print(f"Caught {e}. Retrying in 60 seconds...")
            sleep(60)
            retries += 1
    raise Exception("Maximum number of retries exceeded. Please try again later.")

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
