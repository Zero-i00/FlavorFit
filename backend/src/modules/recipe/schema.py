import strawberry
from typing import List
from database.models.recipe.recipe import RecipeDifficultyEnum, RecipeTypeEnum
from database.models.recipe.ingredient import IngredientUnitEnum
from modules.user.schema import UserOutput


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


@strawberry.input
class RecipeUpdate:
    pass


@strawberry.input
class RecipeCookStepInput:
    order: int
    title: str
    description: str
    recipe_id: int


@strawberry.type
class RecipeCookStepOutput:
    id: int
    order: int
    title: str
    description: str
    recipe_id: int


@strawberry.type
class RecipeIngredientOutput:
    id: int
    quantity: float
    unit: IngredientUnitEnum
    recipe_id: int
    ingredient_id: int


@strawberry.type
class RecipeOutput:
    id: int
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
    calories: float
    author_id: int
    author: UserOutput
    steps: List[RecipeCookStepOutput]
    ingredients: List[RecipeIngredientOutput]
