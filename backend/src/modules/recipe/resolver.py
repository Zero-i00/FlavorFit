import strawberry
from modules.recipe.ingredients.resolver import IngredientQuery, IngredientMutation


@strawberry.type
class RecipeQuery:

    @strawberry.field
    def ingredients(self) -> IngredientQuery:
        return IngredientQuery()


@strawberry.type
class RecipeMutation:

    @strawberry.field
    def ingredients(self) -> IngredientMutation:
        return IngredientMutation()