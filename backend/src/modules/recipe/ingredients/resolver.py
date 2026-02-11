import strawberry
from fastapi import (
    status,
    HTTPException
)

from typing import List, Optional
from config.graphql import ContextInfo
from modules.auth.guards.role import HasRole
from database.models.user.user import RoleEnum
from modules.auth.guards.auth import IsAuthenticated
from modules.recipe.ingredients.service import ingredient_service
from modules.recipe.ingredients.schema import IngredientInput, IngredientUpdate ,IngredientOutput


@strawberry.type
class IngredientQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def list(self, info: ContextInfo) -> List[IngredientOutput]:
        return await ingredient_service.list(info.context.session)
    
    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def retrieve(self, info: ContextInfo, id: int) -> Optional[IngredientOutput]:
        return await ingredient_service.retrieve(info.context.session, id)
    


@strawberry.type
class IngredientMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create(self, info: ContextInfo, obj: IngredientInput) -> IngredientOutput:
        return await ingredient_service.create(info.context.session, obj)
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, id: int, obj: IngredientUpdate) -> IngredientOutput:
        updated = await ingredient_service.update(info.context.session, id, obj)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось найти ингредиент"
            )
        
        return updated

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def destroy(self, info: ContextInfo, id: int) -> None:
        return await ingredient_service.destroy(info.context.session, id)
