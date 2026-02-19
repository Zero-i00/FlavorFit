import strawberry
from typing import List

from config.graphql import ContextInfo
from modules.auth.guards.role import HasRole
from modules.auth.guards.auth import IsAuthenticated
from database.models.user.user import RoleEnum
from modules.recipe.ingredients.service import ingredient_service
from modules.recipe.ingredients.schema import IngredientInput, IngredientUpdate, IngredientOutput


@strawberry.type
class IngredientQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def list(self, info: ContextInfo) -> List[IngredientOutput]:
        ingredients = await ingredient_service.list(info.context.session)
        return [ingredient_service.to_schema(i) for i in ingredients]

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def retrieve(self, info: ContextInfo, ingredient_id: int) -> IngredientOutput:
        ingredient = await ingredient_service.retrieve(info.context.session, ingredient_id)
        return ingredient_service.to_schema(ingredient)


@strawberry.type
class IngredientMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create(self, info: ContextInfo, obj: IngredientInput) -> IngredientOutput:
        ingredient = await ingredient_service.create(info.context.session, obj)
        return ingredient_service.to_schema(ingredient)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, ingredient_id: int, obj: IngredientUpdate) -> IngredientOutput:
        ingredient = await ingredient_service.update(info.context.session, ingredient_id, obj)
        return ingredient_service.to_schema(ingredient)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def destroy(self, info: ContextInfo, ingredient_id: int) -> bool:
        return await ingredient_service.destroy(info.context.session, ingredient_id)
