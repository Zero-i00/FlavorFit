import strawberry
from typing import TypedDict
from database.models.recipe.recipe import RecipeDifficultyEnum, RecipeTypeEnum


@strawberry.input
class RecipeInput:
    title: str
    description: str
    slug: str

    cook_time: int
    prepare_time: int
    serving_time: int

    fats: float
    carbs: float
    proteins: float

    type: RecipeTypeEnum
    difficulty: RecipeDifficultyEnum


class RecipeUpdate():
    pass

@strawberry.type
class RecipeOutput(RecipeInput):
	id: int
	calories: float


@strawberry.input
class RecipeCookStepInput:
    order: int
    title: str
    description: str
    recipe_id: int


@strawberry.type
class RecipeCookStepOutput(RecipeCookStepInput):
    id: int
