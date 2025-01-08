"""
The MemeMaker uses a Pydantic-AI agent to select an appropriate meme template
and generate content based on a recent conversation.
"""

from __future__ import annotations

from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing_extensions import Annotated

load_dotenv()


class MemeTemplate(BaseModel):
    """Metadata about a meme template"""
    id: str
    name: str
    description: str
    example: str

TemplateID = Literal["drake", "db", "yuno", "spiderman", "sadfrog", "jd", "slap"]

TEMPLATES: dict[TemplateID, MemeTemplate] = {
    "drake": MemeTemplate(
        id="drake",
        name="Drake Hotline Bling",
        description="For comparing two things, where the first is rejected and second is preferred",
        example="Top: Manually writing prompts\nBottom: Using structured templates"
    ),
    "db": MemeTemplate(
        id="db",
        name="Distracted Boyfriend",
        description="For showing preference of one thing over another, especially when it's ironic",
        example="Top: Me looking at new frameworks\nBottom: My unfinished projects"
    ),
    "yuno": MemeTemplate(
        id="yuno",
        name="Y U NO",
        description="For expressing frustration with someone for not doing something",
        example="Top: Y U NO\nBottom: use this meme!?"
    ),
    "spiderman": MemeTemplate(
        id="spiderman",
        name="Spider-Man Pointing",
        description="To highlight blame, similarity, irony, or confusion between identical or overlapping roles or entities, often humorously.",
        example="Top: Frontend Developer\nBottom: Backend Developer"
    ),
    "sadfrog": MemeTemplate(
        id="sadfrog",
        name="Feels Bad Man",
        description="For expressing sadness or depression",
        example="Top: lost my keys\nBottom: feels bad man"
    ),
    "jd": MemeTemplate(
        id="jd",
        name="Joseph Ducreux",
        description="For giving commands. Use archaic/Shakespearean language for humor.",
        example="Top: Disregard Females\nBottom: Acquire Currency"
    ),
    "slap": MemeTemplate(
        id="slap",
        name="Slap",
        description="For something that is interrupted suddenly and unpleasantly",
        example="Top: Me trying to enjoy the weekend\nBottom: Monday"
    ),
}

class MemeResponse(BaseModel):
    """Structure for meme generation responses"""

    template: TemplateID = Field(description="The meme template to use")
    top_text: Annotated[str, Field(max_length=100)] = Field(
        description="Top text for the meme"
    )
    bottom_text: Annotated[str, Field(max_length=100)] = Field(
        description="Bottom text for the meme"
    )

def build_system_prompt() -> str:
    """Build the system prompt from template metadata"""
    template_descriptions = "\n".join(
        f"- {t.name} ('{t.id}'): {t.description}\n  Example: {t.example}"
        for t in TEMPLATES.values()
    )
    
    return f"""You are a meme generator. Analyze conversations and create appropriate memes.

Available templates:
{template_descriptions}

Create memes that are funny and/or sarcastic, either summarizing the conversation or making a joke about it. Choose the most appropriate template for the context."""

agent = Agent(
    "openai:gpt-4o-mini",
    result_type=MemeResponse,
    system_prompt=build_system_prompt(),
)

async def generate_meme_url(conversation: str) -> str:
    """Generate a meme URL based on conversation context"""
    result = await agent.run(f"Create a meme for this conversation:\n{conversation}")

    # Convert to URL format
    template = result.data.template
    top = result.data.top_text.replace(" ", "_")
    bottom = result.data.bottom_text.replace(" ", "_")

    return f"https://api.memegen.link/images/{template}/{top}/{bottom}.png"
