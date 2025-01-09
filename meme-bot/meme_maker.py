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

class DrakeMeme(BaseModel):
    """
    Create a Drake meme

    For comparing two things, where the first is rejected and second is preferred
    
    Example:
      Top: Manually writing prompts
      Bottom: Using structured templates
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/drake/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class DistractedBoyfriendMeme(BaseModel):
    """
    Create a Distracted Boyfriend meme

    For showing preference of one thing over another, especially when it's ironic
    
    Example:
      distracted_by: New frameworks
      actor: Me
      distracted_from: My unfinished projects
    """
    distracted_by: str
    actor: str
    distracted_from: str

    def __str__(self):
        return f"https://api.memegen.link/images/db/{escape_text(self.distracted_by)}/{escape_text(self.actor)}/{escape_text(self.distracted_from)}.png"

class YUNOMeme(BaseModel):
    """
    Create a Y U NO meme

    For expressing frustration with someone for not doing something
    
    Example:
      Top: Y U NO
      Bottom: use this meme!?
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/yuno/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class SpidermanMeme(BaseModel):
    """
    Create a Spider-Man Pointing meme

    To highlight blame, similarity, irony, or confusion between identical or overlapping roles
    
    Example:
      Top: Frontend Developer
      Bottom: Backend Developer
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/spiderman/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class SadFrogMeme(BaseModel):
    """
    Create a Feels Bad Man meme

    For expressing sadness or depression
    
    Example:
      Top: lost my keys
      Bottom: feels bad man
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/sadfrog/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class JosephDucreuxMeme(BaseModel):
    """
    Create a Joseph Ducreux meme

    For giving commands. Use archaic/Shakespearean language for humor.
    
    Example:
      Top: Disregard Females
      Bottom: Acquire Currency
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/jd/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class SlapMeme(BaseModel):
    """
    Create a Slap meme

    For something that is interrupted suddenly and unpleasantly
    
    Example:
      Top: Me trying to enjoy the weekend
      Bottom: Monday
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/slap/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class AncientAliensGuyMeme(BaseModel):
    """
    Create an Ancient Aliens Guy meme

    Use this for a ridiculous or far-fetched explanation of something
    
    Example:
      Top: The pyramids?
      Bottom: Aliens
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/aag/{escape_text(self.top)}/{escape_text(self.bottom)}.png"
    
class AstronautMeme(BaseModel):
    """
    Create an Astronaut meme

    This represents someone learning a forbidden or dangerous secret, just when it's too late
    
    Example:
      Top: Wait, it's round?
      Bottom: Always has been
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/astronaut/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class AwesomeMeme(BaseModel):
    """
    Create a Socially Awesome Penguin meme

    Use this for something that is over-the-top awesome
    
    Example:
      Top: say a word wrong
      Bottom: create hilarious inside joke
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/awesome/{escape_text(self.top)}/{escape_text(self.bottom)}.png"

class AwesomeAwkwardMeme(BaseModel):
    """
    Create a Socially Awesome Awkward Penguin meme

    Use this for something that starts out awesome but ends up awkward
    
    Example:
      Top: first day at new job
      Bottom: spill coffee on bossman
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/awesome-awkward/{escape_text(self.top)}/{escape_text(self.bottom)}.png"
    
class AwkwardMeme(BaseModel):
    """
    Create a Socially Awkward Penguin meme

    Use this for something that is over-the-top awkward
    
    Example:
      Top: start telling joke
      Bottom: forget punchline
    """
    top: str
    bottom: str

    def __str__(self):
        return f"https://api.memegen.link/images/awkward/{escape_text(self.top)}/{escape_text(self.bottom)}.png"


agent = Agent(
    "openai:gpt-4o-mini",
    result_type=DrakeMeme | DistractedBoyfriendMeme | YUNOMeme | SpidermanMeme | SadFrogMeme | JosephDucreuxMeme | SlapMeme | AncientAliensGuyMeme | AstronautMeme | AwesomeMeme | AwesomeAwkwardMeme | AwkwardMeme, # type: ignore
    system_prompt="""You are a meme generator.
Analyze the message, consulting the conversation context if necessary, and create an appropriate meme.
Create a meme that is funny and/or sarcastic.
Choose the most appropriate template for the context.""",
    end_strategy="exhaustive",
)


async def generate_meme_url(conversation: str) -> str:
    """Generate a meme URL based on conversation context"""

    # Try up to 3 times
    for _ in range(3):
        result = await agent.run(f"Create a meme for this request:\n{conversation}")
        if result:
            return str(result.data)

    return "https://api.memegen.link/images/sadfrog/meme--bot/failed_again.png"
