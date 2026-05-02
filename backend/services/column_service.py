from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.column import Column
from repositories.column_repo import ColumnRepository
from schemas.column import ColumnCreate, ColumnUpdate


class ColumnService:
    def __init__(self, db: AsyncSession):
        self.repo = ColumnRepository(db)

    async def list_columns(self, user_id: str) -> list[Column]:
        return await self.repo.list(user_id)

    async def create_column(self, user_id: str, data: ColumnCreate) -> Column:
        return await self.repo.create(
            user_id=user_id,
            name=data.name,
            color=data.color,
            position=data.position,
        )

    async def update_column(self, column_id: str, user_id: str, data: ColumnUpdate) -> Column:
        column = await self.repo.get_by_id(column_id, user_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        fields = data.model_dump(exclude_none=True)
        if not fields:
            return column
        return await self.repo.update(column, **fields)

    async def delete_column(self, column_id: str, user_id: str) -> None:
        column = await self.repo.get_by_id(column_id, user_id)
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        if column.is_inbox:
            raise HTTPException(status_code=400, detail="The inbox column cannot be deleted")
        await self.repo.delete(column)