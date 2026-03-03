import asyncio
from models.client import get_model_client
from autogen_core.models import UserMessage

async def test_stream():
    client = get_model_client()
    async for chunk in client.create_stream([UserMessage(content="Say hello", source="user")]):
        print(chunk, end="", flush=True)

asyncio.run(test_stream())