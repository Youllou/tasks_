from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Task
from repositories.column_repo import ColumnRepository
from repositories.task_repo import TaskRepository
from repositories.tag_project_repo import TagRepository, ProjectRepository
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.tasks = TaskRepository(db)
        self.tags = TagRepository(db)
        self.projects = ProjectRepository(db)
        self.columns = ColumnRepository(db)

    async def _resolve_column(self, column_id: str | None, user_id: str) -> str:
        if column_id:
            col = await self.columns.get_by_id(column_id, user_id)
            if not col:
                raise HTTPException(status_code=404, detail="Column not found")
            return column_id
        # fall back to inbox
        inbox = await self.columns.get_inbox(user_id)
        if not inbox:
            raise HTTPException(status_code=500, detail="No inbox column found for user")
        return inbox.id

    async def list_tasks(self, user_id: str, column_id=None, tag_name=None, project_id=None, search=None) -> list[Task]:
        return await self.tasks.get_list(user_id, column_id=column_id, tag_name=tag_name, project_id=project_id,
                                         search=search)

    async def create_task(self, user_id: str, data: TaskCreate) -> Task:
        if data.project_id:
            if not await self.projects.get_by_id(data.project_id, user_id):
                raise HTTPException(status_code=404, detail="Project not found")

        column_id = await self._resolve_column(data.column_id, user_id)

        task = await self.tasks.create(
            user_id=user_id,
            column_id=column_id,
            title=data.title,
            description=data.description,
            due_date=data.due_date,
            project_id=data.project_id,
        )

        if data.tag_ids:
            tags = await self.tags.get_many_by_ids(data.tag_ids, user_id)
            await self.tasks.set_tags(task, tags)

        return task

    async def update_task(self, task_id: str, user_id: str, data: TaskUpdate) -> Task:
        task = await self.tasks.get_by_id(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if data.project_id is not None:
            if data.project_id and not await self.projects.get_by_id(data.project_id, user_id):
                raise HTTPException(status_code=404, detail="Project not found")

        if data.column_id is not None:
            await self._resolve_column(data.column_id, user_id)

        update_fields = data.model_dump(exclude_none=True, exclude={"tag_ids"})
        if update_fields:
            task = await self.tasks.update(task, **update_fields)

        if data.tag_ids is not None:
            tags = await self.tags.get_many_by_ids(data.tag_ids, user_id)
            await self.tasks.set_tags(task, tags)

        return task

    async def delete_task(self, task_id: str, user_id: str) -> None:
        task = await self.tasks.get_by_id(task_id, user_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await self.tasks.delete(task)


class TagService:
    def __init__(self, db: AsyncSession):
        self.repo = TagRepository(db)

    async def list_tags(self, user_id: str):
        return await self.repo.get_list(user_id)

    async def create_tag(self, user_id: str, name: str):
        if await self.repo.get_by_name(name, user_id):
            raise HTTPException(status_code=400, detail="Tag already exists")
        return await self.repo.create(user_id, name)

    async def delete_tag(self, tag_id: str, user_id: str) -> None:
        tag = await self.repo.get_by_id(tag_id, user_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        await self.repo.delete(tag)


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo = ProjectRepository(db)

    async def list_projects(self, user_id: str):
        return await self.repo.list(user_id)

    async def create_project(self, user_id: str, name: str):
        return await self.repo.create(user_id, name)

    async def delete_project(self, project_id: str, user_id: str) -> None:
        project = await self.repo.get_by_id(project_id, user_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        await self.repo.delete(project)