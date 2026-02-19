import strawberry
from typing import List, Optional
from config.graphql import ContextInfo
from modules.recipe.service import recipe_service
from modules.recipe.schema import RecipeOutput
from modules.recipe.ingredients.resolver import IngredientQuery, IngredientMutation
from modules.recipe.comments.resolver import CommentQuery, CommentMutation
from modules.recipe.favorites.resolver import FavoriteQuery, FavoriteMutation


@strawberry.type
class RecipeQuery:

    @strawberry.field
    async def list(self, info: ContextInfo) -> List[RecipeOutput]:
        recipes = await recipe_service.list(info.context.session)
        return [recipe_service.to_schema(r) for r in recipes]

    @strawberry.field
    async def retrieve(self, info: ContextInfo, id: int) -> Optional[RecipeOutput]:
        recipe = await recipe_service.retrieve(info.context.session, id)
        return recipe_service.to_schema(recipe)

    @strawberry.field
    async def get_by_slug(self, info: ContextInfo, slug: str) -> Optional[RecipeOutput]:
        recipe = await recipe_service.get_by_slug(info.context.session, slug)
        return recipe_service.to_schema(recipe)

    @strawberry.field
    def ingredients(self) -> IngredientQuery:
        return IngredientQuery()

    @strawberry.field
    def comments(self) -> CommentQuery:
        return CommentQuery()

    @strawberry.field
    def favorites(self) -> FavoriteQuery:
        return FavoriteQuery()


@strawberry.type
class RecipeMutation:

    @strawberry.field
    def ingredients(self) -> IngredientMutation:
        return IngredientMutation()

    @strawberry.field
    def comments(self) -> CommentMutation:
        return CommentMutation()

    @strawberry.field
    def favorites(self) -> FavoriteMutation:
        return FavoriteMutation()
