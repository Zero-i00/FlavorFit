from typing import List

import strawberry

from config.graphql import ContextInfo
from modules.auth.guards import IsAuthenticated
from modules.recipe.favorites.schema import FavoriteInput, FavoriteOutput
from modules.recipe.favorites.service import favorite_service


@strawberry.type
class FavoriteQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def list(self, info: ContextInfo) -> List[FavoriteOutput]:
        favorites = await favorite_service.list(info.context.session, info.context.user.id)
        return [favorite_service.to_schema(f) for f in favorites]


@strawberry.type
class FavoriteMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create(self, info: ContextInfo, obj: FavoriteInput) -> FavoriteOutput:
        favorite = await favorite_service.create(info.context.session, obj, info.context.user.id)
        return favorite_service.to_schema(favorite)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def destroy(self, info: ContextInfo, recipe_id: int) -> bool:
        return await favorite_service.destroy(info.context.session, recipe_id, info.context.user.id)
