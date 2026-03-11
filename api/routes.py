from fastapi import APIRouter
from pydantic import BaseModel
from core.runner import run_task_stream

router = APIRouter()

class TaskRequest(BaseModel):
    task: str

@router.post("/run")

async def run(request: TaskRequest):
    result = await run_task_stream(request.task)
    return {"result": result}
