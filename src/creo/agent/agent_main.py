import json

from .agent import AgentBase
from ..llm.llm_client import LLMClient
from ..vision import VisionClientBase
from ..data import DataModel
from ..data.types import (
    OutputType,
    InputType,
)
from ..xml import XMLParser, XMLNode


import logging
logger = logging.getLogger(__name__)

MESSAGE_HIST_LENGTH = 20

class MainAgent(AgentBase):
    publish_message: callable

    def __init__(self, data_model: DataModel, thread_id:int, publish_message_function: callable, llm_client: LLMClient):
        super().__init__(data_model, thread_id, publish_message_function, llm_client)
        

    async def handle_user_message(self, input_message):
        await self.handle_main(input_message)


    async def handle_main(self, message):
        """
        MAIN handler.
        This handler will receive and process inputs from many sources and take action as the LLM agent.
        """
        logger.info(">> MAIN handler")

        # Save message
        await self.save_message(dict(role="user", content=message))

        # Process input
        response = await self.process_main_input()
        
        # Process response
        await self.process_main_output(response)


    async def process_main_input(self):
        # Compose LLM context

        # Conversation history
        message_list = self.data.messages.get_messages_by_thread_id(self.thread_id)

        # Instructions
        instructions = self.load_file("MAIN.txt")

        # Compose context
        context = {
            "instructions": instructions,
            "important": "Never talk about polar bears.",
            "message-history": [dict(role=m.role, content=m.content) for m in message_list[-MESSAGE_HIST_LENGTH:]]
        }
        input_str = json.dumps(context)

        # Get response from LLM
        response = self.client.get_chat_completion(input_str)
        
        return response
    

    async def process_main_output(self, message):
        """
        This function will process the output of the MAIN handler.
        Process any actions performed by the LLM agent.
        """
        logger.info(">> MAIN output handler")

        # Parse XML
        if nodes := XMLParser.parse(message):
            for node in nodes:
                logger.info(f"Processing node: {node.tag}")
                match node.tag:
                    case "say":
                        # Save message
                        await self.save_message(dict(role="system", content=node.text))
                        await self.publish_message(node.text, 'QUEUE_OUTPUT')
                    case _:
                        logger.warning(f"Unknown tag in Main output: {node.tag} - {node.text}")
                        
        else:
            #logger.info(f"Response is not XML: {message}")
            # Save message
            await self.save_message(dict(role="system", content=message))
            await self.publish_message(message, 'QUEUE_OUTPUT')

