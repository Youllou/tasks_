import typing

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Tag, Project


class TagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, user_id: str) -> typing.List[Tag]:
        result = await self.db.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        )
        return typing.List(result.scalars())

    async def get_by_id(self, tag_id: str, user_id: str) -> Tag | None:
        result = await self.db.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str, user_id: str) -> Tag | None:
        result = await self.db.execute(
            select(Tag).where(Tag.name == name, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_many_by_ids(self, tag_ids: typing.List[str], user_id: str) -> typing.List[Tag]:
        result = await self.db.execute(
            select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id)
        )
        return typing.List(result.scalars())

    async def create(self, user_id: str, name: str) -> Tag:
        tag = Tag(user_id=user_id, name=name)
        self.db.add(tag)
        await self.db.flush()
        await self.db.refresh(tag)
        return tag

    async def delete(self, tag: Tag) -> None:
        await self.db.delete(tag)
        await self.db.flush()


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, user_id: str) -> typing.List[Project]:
        result = await self.db.execute(
            select(Project).where(Project.user_id == user_id).order_by(Project.name)
        )
        return typing.List(result.scalars())

    async def get_by_id(self, project_id: str, user_id: str) -> Project | None:
        result = await self.db.execute(
            select(Project).where(Project.id == project_id, Project.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: str, name: str) -> Project:
        project = Project(user_id=user_id, name=name)
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()