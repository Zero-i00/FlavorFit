from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.recipe.recipe import RecipeModel
from modules.recipe.schema import RecipeInput, RecipeOutput, RecipeUpdate


class RecipeService:
    def __init__(self) -> None:
        self.not_found_exception = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось найти рецепт"
            )

    async def list(self, session: AsyncSession) -> List[RecipeOutput]:
        query = select(RecipeModel)
        result = await session.execute(query)

        recipes = result.scalars().all()

        return [self.to_schema(recipe) for recipe in recipes]

    async def retrieve(self, session: AsyncSession, id: int) -> Optional[RecipeOutput]:
        recipe = await session.get(RecipeModel, id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.not_found_exception
            )

        return self.to_schema(recipe)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Optional[RecipeOutput]:
        query = select(RecipeModel).where(RecipeModel.slug == slug)
        result = await session.execute(query)

        recipe = result.scalar_one_or_none()
        if not recipe:
            raise self.not_found_exception

        return self.to_schema(recipe)

    async def create(self, session: AsyncSession, obj: RecipeInput) -> RecipeOutput:
        recipe = self.to_model(obj)

        session.add(recipe)
        await session.commit()
        await session.refresh(recipe)

        return self.to_schema(recipe)


    async def update(self, session: AsyncSession, id: int, obj: RecipeUpdate) -> Optional[RecipeOutput]:
        pass

    async def destory(self, session: AsyncSession) -> Optional[RecipeOutput]:
		    pass
			
    @staticmethod
    def to_schema(obj: RecipeModel) -> RecipeOutput:
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
        )

    @staticmethod
    def to_model(obj: RecipeInput) -> RecipeModel:
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
        )



recipe_service = RecipeService()
