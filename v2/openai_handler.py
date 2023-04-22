import openai
import dotenv
import os


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAIHandler:
    def __init__(self, prompt, context=None):
        self.query(prompt, context)

    def query(self, prompt, context=None):
        messages = [
            {"role": "user", "content": "prompt"},
        ]
        # if context:
        #     messages.append({"role": "system", "content": context})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=messages,
        )

        generated_response = response["choices"][0]["message"]["content"]
        return generated_response.strip()
