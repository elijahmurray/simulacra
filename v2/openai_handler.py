import openai


class OpenAIHandler:
    def __init__(self, prompt, context=None):
        return self.query(prompt, context)

    def query(self, prompt, context=None):
        messages = (
            [
                {"role": "user", "content": prompt},
            ],
        )
        if context:
            messages << {"role": "system", "content": context}

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", temperature=0.3, messages=messages
        )

        generated_response = response["choices"][0]["message"]["content"]
        return generated_response.strip()
