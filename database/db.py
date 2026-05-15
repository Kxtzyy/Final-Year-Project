import aiosqlite
from auth import hash_password, verify_password

DB_PATH = "app.db"

async def init_db():
    # Creates the users, conversations, and messages tables if they don't already exist
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id                  INTEGER     PRIMARY KEY     AUTOINCREMENT,
            username            TEXT        NOT NULL        UNIQUE,
            password            TEXT        NOT NULL
            );
        CREATE TABLE IF NOT EXISTS conversations (
            id                  INTEGER     PRIMARY KEY     AUTOINCREMENT,
            user_id             INTEGER     NOT NULL        REFERENCES users(id),
            title               TEXT        NOT NULL        DEFAULT 'New Chat'
            );
        CREATE TABLE IF NOT EXISTS messages (
            id                  INTEGER     PRIMARY KEY     AUTOINCREMENT,
            conversation_id     INTEGER     NOT NULL        REFERENCES conversations(id),
            agent               TEXT        NOT NULL,
            content             TEXT        NOT NULL
            );
        """)
        await db.commit()
async def create_user(username: str, password: str) -> dict | None:
    # Hashes the password before storing; returns None if username is already taken
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))  # hash before storing
            )
            await db.commit()
            return {"id": cursor.lastrowid, "username": username}
    except aiosqlite.IntegrityError:
        return None

async def get_user(username: str, password: str) -> dict | None:
    # Fetches user by username, then verifies the plaintext password against the stored hash
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE username = ?",  # fetch by username only
            (username,)
        )
        row = await cursor.fetchone()
        if row and verify_password(password, row["password"]):
            return dict(row)
        return None

async def del_user(username: str, password: str) -> bool:
    # Verifies credentials before deleting; returns False if user not found or password incorrect
    async with aiosqlite.connect(DB_PATH) as connection:
        connection.row_factory = aiosqlite.Row
        cursor = await connection.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        row = await cursor.fetchone()
        if not row or not verify_password(password, row["password"]):
            return False
        await connection.execute(
            "DELETE FROM users WHERE username = ?", (username,)
        )
        await connection.commit()
        return True

async def create_conversation(user_id : int, title : str = "New Chat") -> dict:
    # Creates a new conversation for the given user with an optional title
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO conversations (user_id, title) VALUES (?, ?)",
            (user_id, title)
        )
        await db.commit()
        return {"id": cursor.lastrowid, "user_id": user_id, "title": title}

async def get_conversations(user_id: int) -> list[dict]:
    # Returns all conversations belonging to the given user
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM conversations WHERE user_id = ?",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def del_conversation(user_id : int, id : int) -> bool:
    # Deletes a conversation by ID, scoped to the given user; returns False if not found
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM conversations WHERE user_id = ? AND id = ?",
            (user_id, id)
        )
        await db.commit()
        return cursor.rowcount > 0
    
async def save_message(conversation_id : int, agent : str, content : str) -> dict:
    # Persists a single agent message to the messages table
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO messages (conversation_id, agent,  content) VALUES (?, ?, ?)",
            (conversation_id, agent, content)
        )
        await db.commit()
        return {"id" : cursor.lastrowid, "conversation_id" : conversation_id, "agent" : agent, "content" : content}
async def get_messages(conversation_id : int) -> list[dict]:
    # Returns all messages for a conversation, ordered by insertion order
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY id",
            (conversation_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    

async def update_conversation_title(id: int, title: str) -> bool:
    # Updates the title of a conversation; returns False if no matching conversation found
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "UPDATE conversations SET title = ? WHERE id = ?",
            (title, id)
        )
        await db.commit()
        return cursor.rowcount > 0