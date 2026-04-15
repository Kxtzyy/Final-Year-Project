from fastapi import APIRouter, Request, HTTPException
from core.runner import run_task_stream
from database import db

router = APIRouter()

@router.post("/run")
async def run(request: Request):
    body = await request.json()
    task = body.get("task")
    return await run_task_stream(task)

@router.post("/register")
async def register(request: Request):
    body = await request.json()
    user = await db.create_user(body["username"], body["password"])
    if user is None:
        raise HTTPException(status_code = 409, detail = "Username already taken")
    return user

@router.post("/login")
async def login(request: Request):
    body = await request.json()
    user = await db.get_user(body["username"], body["password"])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user