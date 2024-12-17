import os
import dotenv
import asyncio
from aio_pika import connect, Message
import json

from creo.messenger.base import MessengerBase
from .llm.llm_client import LLMClient
from .manager import Manager

from logging import getLogger, INFO
logger = getLogger(__name__)
logger.setLevel(INFO)

dotenv.load_dotenv('.env')

class MessageBot():
    def __init__(self, messenger_cls: MessengerBase, client_cls: LLMClient):
        self.messenger = messenger_cls(self.receive_user_message)

        self.loop = asyncio.get_event_loop()
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None

        self.manager = Manager(self.publish_to_rabbitmq, client_cls())

    async def setup(self):
        await self.start_rabbitmq_consumer()

    async def start_rabbitmq_consumer(self):
        self.rabbitmq_connection = await connect(host=os.getenv('RABBITMQ_HOST'))
        self.rabbitmq_channel = await self.rabbitmq_connection.channel()

        queue_list=[
            'QUEUE_OUTPUT',
            'QUEUE_INPUT',
            'MAIN_INPUT',
        ]
        async def consume_queue(queue_name):
            queue = await self.rabbitmq_channel.declare_queue(queue_name, durable=True)
            await queue.purge()
            await queue.consume(self.on_rabbitmq_message)

        # Create a list of tasks to run for each queue
        tasks = [consume_queue(queue_name) for queue_name in queue_list]
        
        # Gather all the consumer tasks to run them concurrently
        await asyncio.gather(*tasks)

    async def publish_to_rabbitmq(self, message_content, routing_key):
        if not self.rabbitmq_channel or self.rabbitmq_channel.is_closed:
            await self.setup()

        message = Message(message_content.encode())
        await self.rabbitmq_channel.default_exchange.publish(
            message, routing_key=routing_key
        )
        print(f"Message sent to RabbitMQ: [{routing_key}]: {message_content}")

    async def on_rabbitmq_message(self, message):
        print(f"Message received from RabbitMQ: [{message.routing_key}]:\n{message.body.decode()}")
        # TODO: Can we move all of this logic to the Manager?
        async with message.process():
            # route message based on routing_key
            match message.routing_key:
                case 'QUEUE_OUTPUT':
                    # Message for output to user
                    await self.messenger.send_user_message(message.body.decode())
                case 'QUEUE_INPUT':
                    # Message from the user to the bot
                    await self.manager.handle_user_message(message.body.decode())
                case 'MAIN_INPUT':
                    # Input to Main handler
                    await self.manager.handle_main(message.body.decode())
                
    async def receive_user_message(self, message: str):
        if message.startswith('!'):
            await self.manager.handle_command(message)
        else:
            await self.publish_to_rabbitmq(message, 'QUEUE_INPUT')

    def run(self):
        # Run the bot
        asyncio.run(self.setup())
        self.messenger.run()
