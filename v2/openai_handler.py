import openai
import dotenv
import os
from colorama import Fore, Back, Style


from helpers import (
    handle_logging,
)


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAIHandler:
    # def __init__(self, prompt, context=None):
    # self.response = self.query(prompt, context)

    def create_embedding(input):
        response = openai.Embedding.create(
            input=input,
            model="text-embedding-ada-002",
        )

        return response

    def chatCompletion(self, prompt, context=None):
        messages = []

        handle_logging("Context: \n" + str(context), type="context")
        handle_logging("\nPrompt: " + prompt, type="prompt")

        if context is not None:
            if isinstance(context, list):
                for message in context:
                    messages.append({"role": "system", "content": message})
            else:
                messages.append({"role": "system", "content": context})

        messages.append(
            {"role": "user", "content": prompt},
        )

        handle_logging("Querying OpenAI...", type="method")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=messages,
        )

        generated_response = response["choices"][0]["message"]["content"].strip()
        handle_logging("Response: \n" + generated_response, type="openai_response")

        return generated_response
