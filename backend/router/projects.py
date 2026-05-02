from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.task import ProjectOut, ProjectCreate
from services.auth_service import get_current_user
from services.task_service import ProjectService

router = APIRouter()


@router.get("", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ProjectService(db).list_projects(current_user.id)


@router.post("", response_model=ProjectOut, status_code=201)
async def create_project(body: ProjectCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ProjectService(db).create_project(current_user.id, body.name)


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await ProjectService(db).delete_project(project_id, current_user.id)