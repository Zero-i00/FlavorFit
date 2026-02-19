from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.recipe.favorite import FavoriteModel
from modules.recipe.favorites.schema import FavoriteInput, FavoriteOutput
from modules.user.service import user_service


class FavoriteService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found",
        )
        self.already_exists_exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recipe already in favorites",
        )

    async def list(self, session: AsyncSession, author_id: int) -> Sequence[FavoriteModel]:
        query = select(FavoriteModel).where(FavoriteModel.author_id == author_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def retrieve(self, session: AsyncSession, favorite_id: int) -> FavoriteModel:
        favorite = await session.get(FavoriteModel, favorite_id)
        if favorite is None:
            raise self.not_found_exception
        return favorite

    async def create(self, session: AsyncSession, obj: FavoriteInput, author_id: int) -> FavoriteModel:
        query = select(FavoriteModel).where(
            FavoriteModel.author_id == author_id,
            FavoriteModel.recipe_id == obj.recipe_id,
        )
        result = await session.execute(query)
        if result.scalar_one_or_none() is not None:
            raise self.already_exists_exception

        favorite = self.to_model(obj, author_id)
        session.add(favorite)
        await session.commit()
        await session.refresh(favorite)

        return favorite

    async def destroy(self, session: AsyncSession, recipe_id: int, author_id: int) -> bool:
        query = select(FavoriteModel).where(
            FavoriteModel.author_id == author_id,
            FavoriteModel.recipe_id == recipe_id,
        )
        result = await session.execute(query)
        favorite = result.scalar_one_or_none()
        if favorite is None:
            raise self.not_found_exception

        await session.delete(favorite)
        await session.commit()
        return True

    @staticmethod
    def to_schema(obj: FavoriteModel) -> FavoriteOutput:
        return FavoriteOutput(
            id=obj.id,
            author_id=obj.author_id,
            author=user_service.to_schema(obj.author),
            recipe_id=obj.recipe_id,
        )

    @staticmethod
    def to_model(obj: FavoriteInput, author_id: int) -> FavoriteModel:
        return FavoriteModel(
            author_id=author_id,
            recipe_id=obj.recipe_id,
        )


favorite_service = FavoriteService()
