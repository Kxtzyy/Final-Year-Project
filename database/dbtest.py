import asyncio

from db import init_db

async def test():
    await init_db()
    print("Initialised")

asyncio.run(test())