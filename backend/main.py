from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from os import getenv

from router import auth, tasks, tags, projects

@asynccontextmanager
async def lifespan(app: FastAPI):
    # app init
    yield # app running
    # app closing

app = FastAPI(title="Tasks_ API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv("CORS_ORIGIN", "127.0.0.1")],
    allow_credentials=True,
    allow_methods=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])


@app.get("/health")
async def health():
    return {"status": "ok"}