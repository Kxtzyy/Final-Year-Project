import asyncio
from auth import hash_password, verify_password
import aiosqlite
import db

async def test():
    await db.init_db()
    print("Database initialised")

    # Test user creation
    user = await db.create_user(username="TestUser", password="test123")
    print(f"Created user: {user}")

    # Test duplicate user
    duplicate = await db.create_user(username="TestUser", password="test123")
    print(f"Duplicate user (should be None): {duplicate}")

    # Test valid login
    valid_login = await db.get_user(username="TestUser", password="test123")
    print(f"Valid login: {valid_login}")

    # Test invalid login
    invalid_login = await db.get_user(username="TestUser", password="wrongpassword")
    print(f"Invalid login (should be None): {invalid_login}")

    # Test conversation creation
    conversation = await db.create_conversation(user_id=valid_login["id"], title="Test Conversation")
    print(f"Created conversation: {conversation}")

    # Test message saving
    message = await db.save_message(conversation["id"], "Coder", "Here is your solution.")
    print(f"Saved message: {message}")

    # Test message retrieval
    messages = await db.get_messages(conversation["id"])
    print(f"Retrieved messages: {messages}")

    # Test conversation retrieval
    conversations = await db.get_conversations(valid_login["id"])
    print(f"Retrieved conversations: {conversations}")

    # Test conversation deletion
    deleted = await db.del_conversation(valid_login["id"], conversation["id"])
    print(f"Deleted conversation (should be True): {deleted}")

    # Test user deletion
    async def del_user(username: str, password: str) -> bool:
        async with aiosqlite.connect(db.DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM users WHERE username = ?", (username,)
            )
            row = await cursor.fetchone()
            if not row or not verify_password(password, row["password"]):
                return False
            await db.execute(
                "DELETE FROM users WHERE username = ?", (username,)
            )
            await db.commit()
            return True

asyncio.run(test())