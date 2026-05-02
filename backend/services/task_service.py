from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Task
from repositories.task_repo import TaskRepository
from repositories.tag_project_repo import TagRepository, ProjectRepository
from schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.tasks = TaskRepository(db)
        self.tags = TagRepository(db)
        self.projects = ProjectRepository(db)

    async def list_tasks(self, user_id: str, status=None, tag_name=None, project_id=None, search=None) -> list[Task]:
        return await self.tasks.list(user_id, status=status, tag_name=tag_name, project_id=project_id, search=search)

    async def create_task(self, user_id: str, data: TaskCreate) -> Task:
        if data.project_id:
            if not await self.projects.get_by_id(data.project_id, user_id):
                raise HTTPException(status_code=404, detail="Project not found")

        task = await self.tasks.create(
            user_id=user_id,
            title=data.title,
            description=data.description,
            status=data.status,
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
        return await self.repo.list(user_id)

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