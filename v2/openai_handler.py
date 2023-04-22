import openai
import dotenv
import os
from colorama import Fore, Back, Style
from APP_CONSTANTS import DEBUG_PROMPTS, DEBUG_CONTEXT


from APP_CONSTANTS import VERBOSE_MODE


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAIHandler:
    def __init__(self, prompt, context=None):
        self.response = self.query(prompt, context)

    def query(self, prompt, context=None):
        messages = []

        if DEBUG_CONTEXT:
            print(f"{Fore.GREEN}\n\nContext: {context}{Style.RESET_ALL}")
        if DEBUG_PROMPTS:
            print(f"{Fore.MAGENTA}\n\nPrompt: {prompt}{Style.RESET_ALL}")

        if isinstance(context, list):
            for message in context:
                messages.append({"role": "system", "content": message})
        else:
            messages.append({"role": "system", "content": context})

        messages.append(
            {"role": "user", "content": prompt},
        )

        if DEBUG_PROMPTS or DEBUG_CONTEXT or VERBOSE_MODE:
            print(f"{Fore.GREEN}Querying OpenAI...{Style.RESET_ALL}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=messages,
        )

        generated_response = response["choices"][0]["message"]["content"]
        return generated_response.strip()
