"""
The MemeMaker uses a Pydantic-AI agent to select an appropriate meme template
and generate content based on a recent conversation.
"""

from __future__ import annotations

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent

load_dotenv()

logfire.configure()

class MemeResponse(BaseModel):
    url: str

def escape_text(text: str) -> str:
    """Escape text for use in a URL"""
    replacements = [
        ('_', '__'),    # Must come first to avoid double-replacing
        ('-', '--'),    # Must come first to avoid double-replacing
        (' ', '_'),     # Spaces to underscores
        ('?', '~q'),
        ('&', '~a'),
        ('%', '~p'),
        ('#', '~h'),
        ('/', '~s'),
        ('\\', '~b'),
        ('<', '~l'),
        ('>', '~g'),
        ('"', "''"),
        ('\n', '~n')
    ]
    
    for old, new in replacements:
        text = text.replace(old, new)
    return text

agent = Agent(
    "openai:gpt-4o-mini",
    result_type=MemeResponse,
    system_prompt="""You are a meme generator.
Analyze conversations and create appropriate memes.
Create memes that are funny and/or sarcastic, either summarizing the conversation or making a joke about it.
Choose the most appropriate template for the context.
Always use a tool.""",
)

@agent.tool_plain
def drake(top: str, bottom: str) -> MemeResponse:
    """
    Create a Drake meme

    For comparing two things, where the first is rejected and second is preferred
    
    Example:
      Top: Manually writing prompts
      Bottom: Using structured templates
    """
    return MemeResponse(url=f"https://api.memegen.link/images/drake/{escape_text(top)}/{escape_text(bottom)}.png")

@agent.tool_plain
def db(distracted_by: str, subject: str, distracted_from: str) -> MemeResponse:
    """
    Create a Distracted Boyfriend meme

    For showing preference of one thing over another, especially when it's ironic
    
    Example:
      distracted_by: New frameworks
      subject: Me
      distracted_from: My unfinished projects
    """
    return MemeResponse(url=f"https://api.memegen.link/images/db/{escape_text(distracted_by)}/{escape_text(subject)}/{escape_text(distracted_from)}.png")

@agent.tool_plain
def yuno(top: str, bottom: str) -> MemeResponse:
    """
    Create a Y U NO meme

    For expressing frustration with someone for not doing something
    
    Example:
      Top: Y U NO
      Bottom: use this meme!?
    """
    return MemeResponse(url=f"https://api.memegen.link/images/yuno/{escape_text(top)}/{escape_text(bottom)}.png")

@agent.tool_plain
def spiderman(top: str, bottom: str) -> MemeResponse:
    """
    Create a Spider-Man Pointing meme

    To highlight blame, similarity, irony, or confusion between identical or overlapping roles
    
    Example:
      Top: Frontend Developer
      Bottom: Backend Developer
    """
    return MemeResponse(url=f"https://api.memegen.link/images/spiderman/{escape_text(top)}/{escape_text(bottom)}.png")

@agent.tool_plain
def sadfrog(top: str, bottom: str) -> MemeResponse:
    """
    Create a Feels Bad Man meme

    For expressing sadness or depression
    
    Example:
      Top: lost my keys
      Bottom: feels bad man
    """
    return MemeResponse(url=f"https://api.memegen.link/images/sadfrog/{escape_text(top)}/{escape_text(bottom)}.png")

@agent.tool_plain
def jd(top: str, bottom: str) -> MemeResponse:
    """
    Create a Joseph Ducreux meme

    For giving commands. Use archaic/Shakespearean language for humor.
    
    Example:
      Top: Disregard Females
      Bottom: Acquire Currency
    """
    return MemeResponse(url=f"https://api.memegen.link/images/jd/{escape_text(top)}/{escape_text(bottom)}.png")

@agent.tool_plain
def slap(top: str, bottom: str) -> MemeResponse:
    """
    Create a Slap meme

    For something that is interrupted suddenly and unpleasantly
    
    Example:
      Top: Me trying to enjoy the weekend
      Bottom: Monday
    """
    return MemeResponse(url=f"https://api.memegen.link/images/slap/{escape_text(top)}/{escape_text(bottom)}.png")

async def generate_meme_url(conversation: str) -> str:
    """Generate a meme URL based on conversation context"""

    # Try up to 3 times
    for _ in range(3):
        result = await agent.run(f"Create a meme for this conversation:\n{conversation}")
        if "api.memegen.link" in result.data.url:
            return result.data.url

    return "https://api.memegen.link/images/sadfrog/meme--bot/failed_again.png"
