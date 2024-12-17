import os
import discord
from discord.ext import commands
import dotenv
import logging

from .base import MessengerBase

logging.basicConfig(level=logging.ERROR)
dotenv.load_dotenv('.env')

MAX_MESSAGE_LENGTH = 2000
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

class DiscordMessenger(commands.Bot, MessengerBase):
    def __init__(self, message_received_callback):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix='!', intents=intents)
        MessengerBase.__init__(self, message_received_callback)

    async def on_message(self, message):
        # if this is a message to someone else, ignore it
        if message.mentions and message.mentions[0] != self.user:
            return

        # if this is a message from the bot, ignore it
        if message.author == self.user:
            return

        # if this message is not in the channel, ignore it
        if message.channel.id != CHANNEL_ID:
            return
        
        # All else: send the message to the bot
        await self.receive_user_message(message.content)

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        await self.send_user_message(f'Logged in as {self.user}!')

    async def send_discord_message(self, message, channel_id=CHANNEL_ID):
        channel = self.get_channel(int(channel_id))
        if not channel:
            print(f"Channel not found: {channel_id}")
            return
        if not self.is_ready():
            await self.wait_until_ready()
        if len(message) < MAX_MESSAGE_LENGTH:
            print(f"Sending message: {message}")
            await channel.send(message)
        else:
            n = 0
            while n < len(message):
                await channel.send(message[n:n+MAX_MESSAGE_LENGTH])
                n += MAX_MESSAGE_LENGTH

    async def send_user_message(self, message):
        await self.send_discord_message(message)

    async def receive_user_message(self, message):
        await self.message_received_callback(message)

    async def send_user_image(self, image_url, description=None):
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Channel not found: {CHANNEL_ID}")
            return
        
        embed = discord.Embed(title=description[:256] or "description")
        embed.set_image(url=image_url)

        print(f"Sending image: {image_url}")
        await channel.send(embed=embed)

    def run(self):
        commands.Bot.run(self, token=os.getenv('DISCORD_TOKEN'), reconnect=True)