import os
from openai import OpenAI

from .llm_client import LLMClient


MODEL_NAME = "gpt-4o-mini"
#MODEL_NAME = "o1-mini"
#MODEL_NAME = "o1-preview"

class LLMClientOpenAI(LLMClient):
    def __init__(self):
        self.client =  self.client=OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def get_chat_completion(self, input_message: str, model_name: str = MODEL_NAME) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_message
                }
            ],
            model=model_name,
        )
        return chat_completion.choices[0].message.content
