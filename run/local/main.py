
import asyncio
import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from creo.bot import MessageBot
from creo.messenger.discord import DiscordMessenger
from creo.llm.llm_openai import LLMClientOpenAI as LLMClient

from logging import basicConfig, getLogger, INFO
basicConfig(level=INFO)

logger = getLogger(__name__)

logger_discord = getLogger("discord.gateway")
# silence
logger_discord.setLevel(40)


if __name__ == '__main__':
    bot = MessageBot(DiscordMessenger, LLMClient, None)
    bot.run()