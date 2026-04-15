import uvicorn
from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from database import db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app : FastAPI):
    await db.init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_methods = ["*"],
        allow_headers = ["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("server:app", host = "0.0.0.0", port = 8000, reload=True)