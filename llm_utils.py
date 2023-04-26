import openai
from config import OPENAI_MODEL, MAX_TOKENS
from dotenv import load_dotenv
import os

# SET UP CLIENT
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_API_KEY")

def call_llm(prompt_template, data: dict, max_tokens=MAX_TOKENS, temperature=0.2):
    '''
    Calls the LLM with a prompt and returns the response text.
    Requires that the data dictionary provided has keys that match the prompt's template variables, or error will be thrown.
    '''
    try:
        prompt = prompt_template.format(**data)
    except KeyError as e:
        raise Exception("The data dictionary provided is missing keys required by the prompt template. Please check the prompt template and the data dictionary provided.")
    response = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
                {"role": "user", "content": prompt}
            ]
        )
    result = response['choices'][0]['message']['content']
    print(result)
    return result

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']
