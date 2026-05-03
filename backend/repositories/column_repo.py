from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.column import Column


DEFAULT_COLUMNS = [
    {"name": "Inbox",   "color": "#4a9eff", "position": 0, "is_inbox": True},
    {"name": "Backlog", "color": "#8b8b9a", "position": 1, "is_inbox": False},
    {"name": "To Do",   "color": "#f5a623", "position": 2, "is_inbox": False},
    {"name": "Done",    "color": "#4caf50", "position": 3, "is_inbox": False},
]


class ColumnRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(self, user_id: str) -> list[Column]:
        result = await self.db.execute(
            select(Column)
            .where(Column.user_id == user_id)
            .order_by(Column.position)
        )
        return list(result.scalars())

    async def get_by_id(self, column_id: str, user_id: str) -> Column | None:
        result = await self.db.execute(
            select(Column).where(Column.id == column_id, Column.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_inbox(self, user_id: str) -> Column | None:
        result = await self.db.execute(
            select(Column).where(Column.user_id == user_id, Column.is_inbox == True)  # noqa: E712
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: str, name: str, color: str, position: int, is_inbox: bool = False) -> Column:
        column = Column(user_id=user_id, name=name, color=color, position=position, is_inbox=is_inbox)
        self.db.add(column)
        await self.db.flush()
        await self.db.refresh(column)
        return column

    async def seed_defaults(self, user_id: str) -> list[Column]:
        """Create the 4 default columns for a new user."""
        columns = []
        for col in DEFAULT_COLUMNS:
            column = await self.create(
                user_id=user_id,
                name=col["name"],
                color=col["color"],
                position=col["position"],
                is_inbox=col["is_inbox"],
            )
            columns.append(column)
        return columns

    async def update(self, column: Column, **kwargs) -> Column:
        for key, value in kwargs.items():
            setattr(column, key, value)
        await self.db.flush()
        await self.db.refresh(column)
        return column

    async def delete(self, column: Column) -> None:
        await self.db.delete(column)
        await self.db.flush()