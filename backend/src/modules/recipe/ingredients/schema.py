from typing import Optional
import strawberry
from strawberry import UNSET
from database.models.recipe.ingredient import IngredientUnitEnum

@strawberry.input
class IngredientInput:
	icon: str
	name: str
	price: float
	description: str
	initial_unit: IngredientUnitEnum
	

@strawberry.input
class IngredientUpdate:
	icon: Optional[str] = UNSET
	name:  Optional[str] = UNSET
	price:  Optional[float] = UNSET
	description:  Optional[str] = UNSET
	initial_unit: Optional[IngredientUnitEnum] = UNSET
	
	
@strawberry.type
class IngredientOutput(IngredientInput):
	id: int
	