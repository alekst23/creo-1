import os
import json

from ..llm.llm_client import LLMClient
from ..data import DataModel
from ..data.types import MessageType
from ..session import Session

import logging
logger = logging.getLogger(__name__)

class AgentBase():
    publish_message: callable
    llm_client : LLMClient
    data: DataModel
    session: Session

    def __init__(self, data_model: DataModel, thread_id: int, publish_message_function: callable, llm_client: LLMClient):
        self.publish_message = publish_message_function
        self.client = llm_client
        self.data = data_model
        self.thread_id = thread_id
        self.session = Session("mock-session-1", self.thread_id)


    @staticmethod
    def load_file(filename):
        path = os.path.join(os.path.dirname(__file__), "config", filename)
        with open(path, "r") as file:
            return file.read()
        

    def publish_message():
        pass

    
    @staticmethod
    def response_from_json(response):
        if response.startswith("```json"):
            response = response[8:-3]
        elif response.startswith("```"):
            response = response[3:-3]
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return response
        

    async def save_message(self, message, character_id=None):
        if type(message) is str:
            try:
                message_obj = json.loads(message)
            except json.JSONDecodeError:
                message_obj = None
        else:
            message_obj = message

        # Store new message
        if message_obj is None or type(message_obj) is str:
            new_message = MessageType(
                thread_id=self.thread_id,
                role="user",
                content=message,
                character_id=character_id
            )
        else:
            new_message = MessageType(
                thread_id=self.thread_id,
                role=message_obj["role"],
                content=message_obj["content"],
                character_id=character_id
            )
        self.data.messages.add_message(new_message)
