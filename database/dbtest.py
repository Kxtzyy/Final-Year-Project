import asyncio

import db

async def test():
    await db.init_db()
    print("Initialised")
    #await db.create_user(username="Yash", password="123")
    await db.del_user(username="Yash", password="123")
    print (await db.get_user(username="Yash", password="123"))
asyncio.run(test())