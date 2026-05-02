from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.column import ColumnOut, ColumnCreate, ColumnUpdate
from services.auth_service import get_current_user
from services.column_service import ColumnService

router = APIRouter()


@router.get("", response_model=list[ColumnOut])
async def list_columns(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ColumnService(db).list_columns(current_user.id)


@router.post("", response_model=ColumnOut, status_code=201)
async def create_column(body: ColumnCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ColumnService(db).create_column(current_user.id, body)


@router.patch("/{column_id}", response_model=ColumnOut)
async def update_column(column_id: str, body: ColumnUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ColumnService(db).update_column(column_id, current_user.id, body)


@router.delete("/{column_id}", status_code=204)
async def delete_column(column_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    await ColumnService(db).delete_column(column_id, current_user.id)