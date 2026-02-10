import strawberry
from fastapi import (
    status,
    HTTPException
)

from config.graphql import ContextInfo

from modules.user.schema import UserOutput

from modules.auth.service import auth_service
from modules.auth.guards.auth import IsAuthenticated
from modules.auth.schema import AuthInput, AuthOutput

@strawberry.type
class AuthQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: ContextInfo) -> UserOutput:
        user = info.context.user
        if not user:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Invalid or expired token"
            )
        
        return user
    

@strawberry.type
class AuthMutation:

    @strawberry.mutation
    async def login(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        response = await auth_service.login(info.context.session, data)

        refresh_token = auth_service.create_refresh_token(response.user)
        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return response
    
    @strawberry.mutation
    async def register(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        response = await auth_service.register(info.context.session, data)

        refresh_token = auth_service.create_refresh_token(response.user)
        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return response