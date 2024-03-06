from openai import OpenAI
from . import schemas


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()

    def send_message(self, msg: schemas.Message):

        response = self.client.chat.completions.create(
            model="gpt-3.5",
            messages=[
                {
                    "role": "system",
                    "content": "You are a tutor. Answer the following question."
                },
                {
                    "role": "user",
                    "content": msg.text
                }
            ],
            temperature=0.8,
            max_tokens=2048,
            top_p=1
        )
        return response
