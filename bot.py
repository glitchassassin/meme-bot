from __future__ import annotations

import discord
from discord.ext import commands
from pydantic import BaseModel, Field
from typing import Literal
from typing_extensions import Annotated
import re
from urllib.parse import quote

# Template IDs we support
MemeTemplate = Literal["drake", "ds", "db"]


class MemeRequest(BaseModel):
    """Structure for meme generation requests"""

    template: MemeTemplate = Field(description="The meme template to use")
    top_text: Annotated[str, Field(max_length=100)] = Field(
        description="Top text for the meme"
    )
    bottom_text: Annotated[str, Field(max_length=100)] = Field(
        description="Bottom text for the meme"
    )

    def to_url(self) -> str:
        """Convert the request to a memegen.link URL"""
        # Escape special characters according to memegen spec
        top = quote(self.top_text.replace(" ", "_"))
        bottom = quote(self.bottom_text.replace(" ", "_"))
        return f"https://api.memegen.link/images/{self.template}/{top}/{bottom}.png"


class MemeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(command_prefix="!", intents=intents)

    async def get_recent_messages(
        self, channel: discord.TextChannel, limit: int = 5
    ) -> str:
        """Get recent message context as a single string"""
        messages = []
        async for msg in channel.history(limit=limit):
            # Skip bot messages and the trigger message
            if not msg.author.bot and not msg.content.strip().lower() == "meme this":
                messages.append(f"{msg.author.name}: {msg.content}")
        return "\n".join(reversed(messages))

    async def generate_meme_request(self, context: str) -> MemeRequest:
        """Analyze context and generate appropriate meme parameters"""
        # For this example we'll use a simple heuristic:
        # If we see "vs" or "versus", use drake template
        # If we see "!" or multiple caps words, use ds (disaster girl)
        # Otherwise use db (distracted boyfriend)

        if re.search(r"\bvs\b|\bversus\b", context.lower()):
            parts = re.split(r"\bvs\b|\bversus\b", context.lower(), maxsplit=1)
            return MemeRequest(
                template="drake",
                top_text=parts[0].strip(),
                bottom_text=parts[1].strip() if len(parts) > 1 else "everything else",
            )
        elif "!" in context or len(re.findall(r"\b[A-Z]{2,}\b", context)) > 1:
            return MemeRequest(
                template="ds", top_text="Time to", bottom_text="Make a meme about this"
            )
        else:
            return MemeRequest(
                template="db", top_text="Me", bottom_text="Making memes from chat"
            )


bot = MemeBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if bot was mentioned with "meme this"
    if bot.user in message.mentions and "meme this" in message.content.lower():
        async with message.channel.typing():
            # Get recent conversation context
            context = await bot.get_recent_messages(message.channel)

            # Generate meme parameters based on context
            meme_request = await bot.generate_meme_request(context)

            # Get the meme URL
            meme_url = meme_request.to_url()

            # Send the meme
            await message.channel.send(meme_url)

    await bot.process_commands(message)


def main():
    bot.run("YOUR_DISCORD_BOT_TOKEN")


if __name__ == "__main__":
    main()
