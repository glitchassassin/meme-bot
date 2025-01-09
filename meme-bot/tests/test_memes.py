import pytest
from meme_maker import generate_meme_url

async def test_distracted_boyfriend_meme():
    url = await generate_meme_url("""Create a meme for this request:
Current message:
lord_greywether: <@1326647991620341781> Create a meme about getting distracted from productive work by meme bots
Conversation context:""")
    assert "https://api.memegen.link/images/db/" in url

async def test_ignores_context_if_not_needed():
    url = await generate_meme_url("""Create a meme for this request:
Current message:
lord_greywether: <@1326647991620341781> Now create a meme about preferring cats to dogs
Conversation context:
lord_greywether: <@1326647991620341781> Create a meme about getting distracted from productive work by meme bots""")
    assert "meme bots" not in url
    assert "productive work" not in url

async def test_uses_context_if_needed():
    url = await generate_meme_url("""Create a meme for this request:
Current message:
lord_greywether: <@1326647991620341781> meme this
Conversation context:
lord_greywether: <@1326647991620341781> I've been getting distracted from productive work by meme bots""")
    assert "https://api.memegen.link/images/db/" in url
