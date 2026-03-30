from fastapi import APIRouter, Request
from core.runner import run_task_stream

router = APIRouter()

@router.post("/run")
async def run(request: Request):
    body = await request.json()
    task = body.get("task")
    return await run_task_stream(task)