import strawberry
from typing import List, Optional

from config.graphql import ContextInfo
from modules.auth.guards.role import HasRole
from modules.auth.guards.auth import IsAuthenticated
from modules.user.service import user_service
from modules.user.schema import UserUpdate, UserOutput, RoleEnum


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


@strawberry.type
class UserMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, user_id: int, obj: UserUpdate) -> UserOutput:
        user = await user_service.update(info.context.session, user_id, obj)
        return user_service.to_schema(user)
