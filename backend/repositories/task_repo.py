from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.task import Task, Tag


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _with_relations(self):
        return selectinload(Task.tags)

    async def get_by_id(self, task_id: str, user_id: str) -> Task | None:
        result = await self.db.execute(
            select(Task)
            .options(self._with_relations())
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        user_id: str,
        column_id: str | None = None,
        tag_name: str | None = None,
        project_id: str | None = None,
        search: str | None = None,
    ) -> list[Task]:
        query = (
            select(Task)
            .options(self._with_relations())
            .where(Task.user_id == user_id)
        )
        if column_id:
            query = query.where(Task.column_id == column_id)  
        if project_id:
            query = query.where(Task.project_id == project_id)
        if search:
            query = query.where(Task.title.ilike(f"%{search}%"))
        if tag_name:
            query = query.join(Task.tags).where(Tag.name == tag_name)

        query = query.order_by(Task.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().unique())

    async def create(self, user_id: str, column_id: str, title: str, **kwargs) -> Task:
        task = Task(user_id=user_id, column_id=column_id, title=title, **kwargs)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task, ["tags"])
        return task

    async def update(self, task: Task, **kwargs) -> Task:
        for key, value in kwargs.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task, ["tags"])
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()

    async def set_tags(self, task: Task, tags: list[Tag]) -> None:
        task.tags = tags
        await self.db.flush()
        await self.db.refresh(task, ["tags"])
