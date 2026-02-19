from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import UNSET

from database.models import IngredientModel
from database.models.recipe.ingredient import IngredientModel
from modules.recipe.ingredients.schema import IngredientInput, IngredientUpdate, IngredientOutput


class IngredientService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )

    async def list(self, session: AsyncSession) -> Sequence[IngredientModel]:
        query = select(IngredientModel)
        result = await session.execute(query)
        return result.scalars().all()

    async def retrieve(self, session: AsyncSession, ingredient_id: int) -> type[IngredientModel]:
        ingredient = await session.get(IngredientModel, ingredient_id)
        if ingredient is None:
            raise self.not_found_exception
        return ingredient

    async def create(self, session: AsyncSession, obj: IngredientInput) -> IngredientModel:
        ingredient = self.to_model(obj)

        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)

        return ingredient

    async def update(self, session: AsyncSession, ingredient_id: int, obj: IngredientUpdate) -> type[IngredientModel]:
        ingredient = await self.retrieve(session, ingredient_id)

        for field, value in vars(obj).items():
            if value is UNSET:
                continue
            if hasattr(ingredient, field):
                setattr(ingredient, field, value)

        session.add(ingredient)
        await session.commit()
        await session.refresh(ingredient)

        return ingredient

    async def destroy(self, session: AsyncSession, ingredient_id: int) -> bool:
        ingredient = await self.retrieve(session, ingredient_id)
        await session.delete(ingredient)
        await session.commit()
        return True

    @staticmethod
    def to_schema(obj: IngredientModel) -> IngredientOutput:
        return IngredientOutput(
            id=obj.id,
            icon=obj.icon,
            name=obj.name,
            price=obj.price,
            description=obj.description,
            initial_unit=obj.initial_unit,
        )

    @staticmethod
    def to_model(obj: IngredientInput) -> IngredientModel:
        return IngredientModel(
            icon=obj.icon,
            name=obj.name,
            price=obj.price,
            description=obj.description,
            initial_unit=obj.initial_unit,
        )


ingredient_service = IngredientService()
