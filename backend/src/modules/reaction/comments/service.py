from typing import List, Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import UNSET

from database.models import CommentModel
from modules.reaction.comments.schema import CommentOutput, CommentInput, CommentUpdate


class CommentService:

    async def list(self, session: AsyncSession) -> List[CommentOutput]:
        query = select(CommentModel)
        result = await session.execute(query)

        comments = result.scalars().all()
        return [self.to_schema(comment) for comment in comments]

    async def retrieve(self, session: AsyncSession, comment_id: int) -> Optional[CommentOutput]:
        comment = await session.get(CommentModel, comment_id)
        return self.to_schema(comment) if comment else None

    async def create(self, session: AsyncSession, obj: CommentInput) -> CommentOutput:
        comment = self.to_model(obj)

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        return self.to_schema(comment)

    async def update(self, session: AsyncSession, comment_id: int, obj: CommentUpdate) -> Optional[CommentOutput]:
        comment = await session.get(CommentModel, comment_id)

        if not comment:
            return None

        for field, value in vars(obj).items():
            if value is UNSET:
                continue

            if hasattr(comment, field):
                setattr(comment, field, value)

        session.add(comment)

        await session.commit()
        await session.refresh(comment)

        return self.to_schema(comment)


    async def destroy(self, session: AsyncSession, comment_id: int) -> None:
        query = delete(CommentModel).where(CommentModel.id == comment_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    def to_schema(obj: type[CommentModel]) -> CommentOutput:
        return CommentOutput(
            id = obj.id,
            content=obj.content,
            author=obj.author,
            recipe=obj.recipe,
        )

    @staticmethod
    def to_model(obj: CommentInput) -> CommentModel:
        return CommentModel(
            content = obj.content,
            author_id=obj.author_id,
            recipe_id=obj.recipe_id,
        )


comment_service = CommentService()
