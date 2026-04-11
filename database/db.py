import aiosqlite

DB_PATH = "app.db"

async def init_db():
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
            content             TEXT        NOT NULL
            );
        """)