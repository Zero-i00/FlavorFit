import strawberry
from typing import List, Optional
from config.graphql import ContextInfo
from modules.recipe.service import recipe_service
from modules.recipe.schema import RecipeInput, RecipeOutput
from modules.recipe.ingredients.resolver import IngredientQuery, IngredientMutation


@strawberry.type
class RecipeQuery:

    @strawberry.field
    async def list(self, info: ContextInfo) -> List[RecipeOutput]:
        return await recipe_service.list(info.context.session)
    
    @strawberry.field
    async def retrieve(self, info: ContextInfo, id: int) -> Optional[RecipeOutput]:
        return await recipe_service.retrieve(info.context.session, id)

    @strawberry.field
    async def get_by_slug(self, info: ContextInfo, slug: str) -> Optional[RecipeOutput]:
        return await recipe_service.get_by_slug(info.context.session, slug)

    @strawberry.field
    def ingredients(self) -> IngredientQuery:
        return IngredientQuery()


@strawberry.type
class RecipeMutation:

    @strawberry.field
    def ingredients(self) -> IngredientMutation:
        return IngredientMutation()