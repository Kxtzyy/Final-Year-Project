from fastapi import APIRouter, Request, HTTPException
from core.runner import run_task_stream
from database import db

router = APIRouter()

# Runs the agent pipeline with the given task and optional conversation ID
@router.post("/run")
async def run(request: Request):
    body = await request.json()
    task = body.get("task")
    conversation_id = body.get("conversation_id")
    print(f"conversation_id from request: {conversation_id}")
    return await run_task_stream(task, conversation_id)

# Registers a new user, returns 409 if username is already taken
@router.post("/register")
async def register(request: Request):
    body = await request.json()
    user = await db.create_user(body["username"], body["password"])
    if user is None:
        raise HTTPException(status_code = 409, detail = "Username already taken")
    return user

# Validates credentials and returns the user object, or 401 if invalid
@router.post("/login")
async def login(request: Request):
    body = await request.json()
    user = await db.get_user(body["username"], body["password"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

# Creates a new conversation for the given user
@router.post("/conversations")
async def new_conversation(request: Request):
    body = await request.json()
    conversation = await db.create_conversation(body["user_id"], body.get("title", "New Chat"))
    return conversation

# Returns all conversations belonging to the given user
@router.get("/conversations/{user_id}")
async def get_conversations(user_id: int):
    conversations = await db.get_conversations(user_id)
    return conversations

# Deletes a conversation by ID, returns 404 if not found
@router.delete("/conversations/{user_id}/{conversation_id}")
async def delete_conversation(user_id: int, conversation_id: int):
    success = await db.del_conversation(user_id, conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"deleted": conversation_id}

# Saves a new message to the given conversation
@router.post("/messages")
async def new_message(request: Request):
    body = await request.json()
    message = await db.save_message(body["conversation_id"], body["agent"], body["content"])
    return message

# Returns all messages for the given conversation, ordered by ID
@router.get("/messages/{conversation_id}")
async def list_messages(conversation_id: int):
    messages = await db.get_messages(conversation_id)
    return messages

# Updates the title of a conversation, returns 404 if not found
@router.patch("/conversations/{conversation_id}")
async def update_conversation(conversation_id: int, request: Request):
    body = await request.json()
    success = await db.update_conversation_title(conversation_id, body["title"])
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"id": conversation_id, "title": body["title"]}