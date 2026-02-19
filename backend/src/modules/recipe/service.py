from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.recipe.recipe import RecipeModel
from modules.recipe.schema import (
    RecipeInput, RecipeOutput,
    RecipeCookStepOutput, RecipeIngredientOutput,
)
from modules.user.service import user_service


class RecipeService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )

    async def list(self, session: AsyncSession) -> Sequence[RecipeModel]:
        query = select(RecipeModel)
        result = await session.execute(query)
        return result.scalars().all()

    async def retrieve(self, session: AsyncSession, id: int) -> RecipeModel:
        recipe = await session.get(RecipeModel, id)
        if recipe is None:
            raise self.not_found_exception
        return recipe

    async def get_by_slug(self, session: AsyncSession, slug: str) -> RecipeModel:
        query = select(RecipeModel).where(RecipeModel.slug == slug)
        result = await session.execute(query)

        recipe = result.scalar_one_or_none()
        if recipe is None:
            raise self.not_found_exception

        return recipe

    @staticmethod
    def to_schema(obj: RecipeModel) -> RecipeOutput:
        steps = [
            RecipeCookStepOutput(
                id=s.id,
                order=s.order,
                title=s.title,
                description=s.description,
                recipe_id=s.recipe_id,
            )
            for s in obj.steps
        ]

        ingredients = [
            RecipeIngredientOutput(
                id=i.id,
                quantity=i.quantity,
                unit=i.unit,
                recipe_id=i.recipe_id,
                ingredient_id=i.ingredient_id,
            )
            for i in obj.ingredients
        ]

        return RecipeOutput(
            id=obj.id,
            slug=obj.slug,
            title=obj.title,
            description=obj.description,
            cook_time=obj.cook_time,
            prepare_time=obj.prepare_time,
            serving_time=obj.serving_time,
            fats=obj.fats,
            carbs=obj.carbs,
            proteins=obj.proteins,
            type=obj.type,
            difficulty=obj.difficulty,
            calories=obj.calories,
            author_id=obj.author_id,
            author=user_service.to_schema(obj.author),
            steps=steps,
            ingredients=ingredients,
        )

    @staticmethod
    def to_model(obj: RecipeInput, author_id: int) -> RecipeModel:
        return RecipeModel(
            title=obj.title,
            description=obj.description,
            slug=obj.slug,
            cook_time=obj.cook_time,
            prepare_time=obj.prepare_time,
            serving_time=obj.serving_time,
            fats=obj.fats,
            carbs=obj.carbs,
            proteins=obj.proteins,
            type=obj.type,
            difficulty=obj.difficulty,
            author_id=author_id,
        )


recipe_service = RecipeService()
