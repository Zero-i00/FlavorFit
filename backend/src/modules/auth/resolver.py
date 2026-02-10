import strawberry
from fastapi import (
    Request,
    status,
    HTTPException
)

from config.graphql import ContextInfo

from modules.user.schema import UserOutput

from modules.auth.service import auth_service
from modules.auth.guards.auth import IsAuthenticated
from modules.auth.schema import AuthInput, AuthOutput, AuthTokenEnum


invalid_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid jwt token",
    )
        

@strawberry.type
class AuthQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def me(self, info: ContextInfo) -> UserOutput:
        user = info.context.user
        if not user:
            raise invalid_token_exception
        
        return user
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def refresh_token(self, info: ContextInfo) -> AuthOutput:
        if not info.context.request or not isinstance(info.context.request, Request):
            raise invalid_token_exception
        
        response = await auth_service.refresh_token(info.context.session, info.context.request)

        refresh_token = auth_service.create_refresh_token(response.user)

        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return response


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
    
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def logout(self, info: ContextInfo) -> None:
        if not info.context.request or not isinstance(info.context.request, Request):
            raise invalid_token_exception
        
        refresh_token = info.context.request.cookies.get(AuthTokenEnum.REFRESH_TOKEN.value) or ""
        if info.context.response:
            info.context.response.delete_cookie(AuthTokenEnum.REFRESH_TOKEN.value)

        return await auth_service.logout(info.context.session, refresh_token)
