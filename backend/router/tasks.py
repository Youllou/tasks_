from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.task import TaskOut, TaskCreate, TaskUpdate
from services.auth_service import get_current_user
from services.task_service import TaskService

router = APIRouter()


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    column_id: str | None = Query(None),
    tag: str | None = Query(None),
    project_id: str | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await TaskService(db).list_tasks(
        current_user.id, column_id=column_id, tag_name=tag, project_id=project_id, search=search
    )


@router.post("", response_model=TaskOut, status_code=201)
async def create_task(body: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await TaskService(db).create_task(current_user.id, body)


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, body: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await TaskService(db).update_task(task_id, current_user.id, body)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await TaskService(db).delete_task(task_id, current_user.id)