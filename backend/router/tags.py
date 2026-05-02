from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.task import TagOut, TagCreate
from services.auth_service import get_current_user
from services.task_service import TagService

router = APIRouter()


@router.get("", response_model=list[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await TagService(db).list_tags(current_user.id)


@router.post("", response_model=TagOut, status_code=201)
async def create_tag(body: TagCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await TagService(db).create_tag(current_user.id, body.name)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await TagService(db).delete_tag(tag_id, current_user.id)