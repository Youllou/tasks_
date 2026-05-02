from datetime import datetime

from pydantic import BaseModel


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
    column_id: str
    project_id: str | None
    title: str
    description: str | None
    due_date: datetime | None
    tags: list[TagOut]
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    column_id: str | None = None   # defaults to user's inbox column in the service
    due_date: datetime | None = None
    project_id: str | None = None
    tag_ids: list[str] = []


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    column_id: str | None = None
    due_date: datetime | None = None
    project_id: str | None = None
    tag_ids: list[str] | None = None