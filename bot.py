from __future__ import annotations

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from meme_maker import generate_meme_url

load_dotenv()

logging.basicConfig(level=logging.INFO)

class MemeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix="!", intents=intents)

    async def get_recent_messages(
        self, message: discord.Message, limit: int = 5
    ) -> str:
        """Get recent message context as a single string"""
        messages = []
        
        # Handle reply scenario
        if message.reference and isinstance(message.reference.resolved, discord.Message):
            messages.extend([
                f"{message.reference.resolved.author.name}: {message.reference.resolved.content}",
                f"{message.author.name}: {message.content}"
            ])
        else:
            # Get recent messages if not a reply
            async for msg in message.channel.history(limit=limit):
                if not msg.author.bot:
                    messages.append(f"{msg.author.name}: {msg.content}")
        
        return "\n".join(reversed(messages))


bot = MemeBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    if bot.user in message.mentions and isinstance(message.channel, discord.TextChannel):
        async with message.channel.typing():
            # Get recent conversation context
            context = await bot.get_recent_messages(message)

            try:
                # Generate meme URL using AI
                meme_url = await generate_meme_url(context)
                # Send the meme
                await message.channel.send(meme_url)
            except Exception as e:
                logging.error(f"Error generating meme: {e}")
                await message.channel.send("I'm broken. Please send help!")


    await bot.process_commands(message)


def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN not found in environment variables")
    bot.run(token)


if __name__ == "__main__":
    main()
