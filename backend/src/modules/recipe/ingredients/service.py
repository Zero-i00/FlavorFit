from typing import List
from strawberry import UNSET
from typing_extensions import Optional
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.recipe.ingredient import IngredientModel
from modules.recipe.ingredients.schema import IngredientInput, IngredientUpdate, IngredientOutput

class IngredientService:
	
	async def list(self, session: AsyncSession) -> List[IngredientOutput]:
		query = select(IngredientModel)
		result = await session.execute(query)
		
		ingredients = result.scalars().all()
		
		return [self.to_schema(obj) for obj in ingredients]
		
		
	async def retrieve(self, session: AsyncSession, id: int) -> Optional[IngredientOutput]:
		ingredient = await session.get(IngredientModel, id)
		return self.to_schema(ingredient) if ingredient else None
		
		
	async def create(self, session: AsyncSession, obj: IngredientInput) -> IngredientOutput:
		ingredient = self.to_model(obj)

		session.add(ingredient)
		await session.commit()
		await session.refresh(ingredient)

		return self.to_schema(ingredient)
	
	async def update(self, session: AsyncSession, id: int, obj: IngredientUpdate) -> Optional[IngredientOutput]:
		ingredient = await session.get(IngredientModel, id)

		if not ingredient:
			return None
		
		for field, value in vars(obj).items():
			print(field, value)
			if value is UNSET:
				continue

			if hasattr(ingredient, field):
				setattr(ingredient, field, value)

		session.add(ingredient)

		await session.commit()
		await session.refresh(ingredient)

		return self.to_schema(ingredient)
	
	async def destroy(self, session: AsyncSession, id: int) -> None:
		query = delete(IngredientModel).where(IngredientModel.id == id)
		await session.execute(query)
		await session.commit()
	
	
	@staticmethod
	def to_schema(obj: IngredientModel) -> IngredientOutput:
		return IngredientOutput(
			id=obj.id,
			icon=obj.icon,
			name=obj.name,
			price=obj.price,
			description=obj.description,
			initial_unit=obj.initial_unit
		)
	
	@staticmethod
	def to_model(obj: IngredientInput) -> IngredientModel:
		return IngredientModel(
			icon=obj.icon,
			name=obj.name,
			price=obj.price,
			description=obj.description,
			initial_unit=obj.initial_unit
		)
		
	
	
	
ingredient_service = IngredientService()
