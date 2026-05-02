from datetime import datetime
from typing import Literal

from pydantic import BaseModel

TaskStatus = Literal["inbox", "backlog", "todo", "done"]


# --- Tag ---

class TagOut(BaseModel):
    id: str
    name: str
    model_config = {"from_attributes": True}


class TagCreate(BaseModel):
    name: str


# --- Project ---

class ProjectOut(BaseModel):
    id: str
    name: str
    created_at: datetime
    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    name: str


# --- Task ---

class TaskOut(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime | None
    project_id: str | None
    tags: list[TagOut]
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = "inbox"
    due_date: datetime | None = None
    project_id: str | None = None
    tag_ids: list[str] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    due_date: datetime | None = None
    project_id: str | None = None
    tag_ids: list[str] | None = None