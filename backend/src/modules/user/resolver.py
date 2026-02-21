import strawberry
from typing import List, Optional

from config.graphql import ContextInfo
from modules.auth.guards.role import HasRole
from modules.auth.guards.auth import IsAuthenticated
from modules.user.service import user_service
from modules.user.schema import UserUpdate, UserOutput, RoleEnum
from modules.recipe.service import recipe_service
from modules.recipe.schema import RecipeOutput
from modules.recipe.comments.service import comment_service
from modules.recipe.comments.schema import CommentOutput
from modules.recipe.favorites.service import favorite_service
from modules.recipe.favorites.schema import FavoriteOutput


@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum.ADMIN)])
    async def list(self, info: ContextInfo) -> List[UserOutput]:
        users = await user_service.list(info.context.session)
        return [user_service.to_schema(u) for u in users]

    @strawberry.field(permission_classes=[HasRole(RoleEnum.ADMIN)])
    async def retrieve(self, info: ContextInfo, user_id: int) -> UserOutput:
        user = await user_service.retrieve(info.context.session, user_id)
        return user_service.to_schema(user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def profile(self, info: ContextInfo) -> UserOutput:
        return user_service.to_schema(info.context.user)

    @strawberry.field
    async def get_by_email(self, info: ContextInfo, email: str) -> Optional[UserOutput]:
        user = await user_service.get_by_email(info.context.session, email)
        if user is None:
            raise user_service.not_found_exception
        return user_service.to_schema(user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def recipes(self, info: ContextInfo, user_id: int) -> List[RecipeOutput]:
        recipes = await recipe_service.list_by_user(info.context.session, user_id)
        return [recipe_service.to_schema(r) for r in recipes]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def comments(self, info: ContextInfo, user_id: int) -> List[CommentOutput]:
        comments = await comment_service.list_by_user(info.context.session, user_id)
        return [comment_service.to_schema(c) for c in comments]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def favorites(self, info: ContextInfo) -> List[FavoriteOutput]:
        favorites = await favorite_service.list(info.context.session, info.context.user.id)
        return [favorite_service.to_schema(f) for f in favorites]


@strawberry.type
class UserMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, user_id: int, obj: UserUpdate) -> UserOutput:
        user = await user_service.update(info.context.session, user_id, obj)
        return user_service.to_schema(user)
