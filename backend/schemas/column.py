from datetime import datetime

from pydantic import BaseModel


class ColumnOut(BaseModel):
    id: str
    name: str
    color: str
    position: int
    is_inbox: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class ColumnCreate(BaseModel):
    name: str
    color: str = "#8b8b9a"
    position: int


class ColumnUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    position: int | None = None