from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import UNSET

from database.models.recipe.comment import CommentModel
from modules.recipe.comments.schema import CommentOutput, CommentInput, CommentUpdate
from modules.user.service import user_service


class CommentService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    async def list(self, session: AsyncSession) -> Sequence[CommentModel]:
        query = select(CommentModel)
        result = await session.execute(query)
        return result.scalars().all()

    async def retrieve(self, session: AsyncSession, comment_id: int) -> CommentModel:
        comment = await session.get(CommentModel, comment_id)
        if comment is None:
            raise self.not_found_exception
        return comment

    async def create(self, session: AsyncSession, obj: CommentInput, author_id: int) -> CommentModel:
        comment = self.to_model(obj, author_id)

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        return comment

    async def update(self, session: AsyncSession, comment_id: int, obj: CommentUpdate) -> CommentModel:
        comment = await self.retrieve(session, comment_id)

        for field, value in vars(obj).items():
            if value is UNSET:
                continue
            if hasattr(comment, field):
                setattr(comment, field, value)

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        return comment

    async def destroy(self, session: AsyncSession, comment_id: int) -> bool:
        comment = await self.retrieve(session, comment_id)
        await session.delete(comment)
        await session.commit()
        return True

    @staticmethod
    def to_schema(obj: CommentModel) -> CommentOutput:
        return CommentOutput(
            id=obj.id,
            content=obj.content,
            recipe_id=obj.recipe_id,
            author_id=obj.author_id,
            author=user_service.to_schema(obj.author),
        )

    @staticmethod
    def to_model(obj: CommentInput, author_id: int) -> CommentModel:
        return CommentModel(
            content=obj.content,
            author_id=author_id,
            recipe_id=obj.recipe_id,
        )


comment_service = CommentService()
