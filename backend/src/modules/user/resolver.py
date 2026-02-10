import strawberry
from fastapi import (
    status,
    HTTPException
)
from typing import List, Optional
from config.graphql import ContextInfo
from modules.auth.guards.role import HasRole
from modules.user.service import user_service
from modules.user.schema import UserOutput, RoleEnum, UserUpdate

not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Не удалось найти пользователя"
)

@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum.ADMIN)])
    async def list(self, info: ContextInfo) -> List[UserOutput]:
        return await user_service.list(info.context.session)
    
    @strawberry.field
    async def retrieve(self, info: ContextInfo, id: int) -> Optional[UserOutput]:
        instance = await user_service.retrieve(info.context.session, id)
        if instance is None:
            raise not_found_exception
        
        return instance
    
    @strawberry.field
    async def get_by_email(self, info: ContextInfo, email: str) -> Optional[UserOutput]:
        instance = await user_service.get_by_email(info.context.session, email)
        if instance is None:
            raise not_found_exception
        
        return instance


@strawberry.type
class UserMutation:
    
    @strawberry.mutation
    async def update(self, info: ContextInfo, id: int, obj: UserUpdate) -> Optional[UserOutput]:
        updated = await user_service.update(info.context.session, id, obj)
        if updated is None:
            raise not_found_exception
        
        return updated
