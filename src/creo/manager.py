from typing import Callable, Optional
import json
import uuid
import asyncio

from .data import DataModel
from .data.types import (
    OutputType,
)
from .llm.llm_client import LLMClient
from .agent.agent_main import MainAgent

from logging import getLogger
logger = getLogger(__name__)


class Manager():
    data: DataModel
    publish_to_rabbitmq: Callable
    client: LLMClient
    agent: MainAgent

    def __init__(self, publish_to_rabbitmq: Callable, client: LLMClient, thread_id: str=None):
        self.data = DataModel()
        self.publish_message = publish_to_rabbitmq
        self.client = client

        if thread_id:
            self.new_session(thread_id)
        else:
            self.new_session(str(uuid.uuid4()) )


    def new_session(self, thread_id):
        self.thread_id = thread_id
        self.agent = MainAgent(self.data, self.thread_id, self.publish_message, self.client, self.vision)


    async def handle_user_message(self, message):
        await self.agent.handle_user_message(message)


    async def handle_main(self, message):
        await self.agent.handle_main(message)
