import strawberry
from fastapi import Request

from config.graphql import ContextInfo
from modules.user.service import user_service
from modules.auth.service import auth_service
from modules.auth.guards.auth import IsAuthenticated
from modules.auth.schema import AuthInput, AuthOutput, AuthTokenEnum


@strawberry.type
class AuthQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def refresh_token(self, info: ContextInfo) -> AuthOutput:
        user = await auth_service.refresh_token(info.context.session, info.context.request)

        access_token = auth_service.create_access_token(user)
        refresh_token = auth_service.create_refresh_token(user)

        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return AuthOutput(
            user=user_service.to_schema(user),
            access_token=access_token,
        )


@strawberry.type
class AuthMutation:

    @strawberry.mutation
    async def login(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        user = await auth_service.login(info.context.session, data)

        access_token = auth_service.create_access_token(user)
        refresh_token = auth_service.create_refresh_token(user)

        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return AuthOutput(
            user=user_service.to_schema(user),
            access_token=access_token,
        )

    @strawberry.mutation
    async def register(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        user = await auth_service.register(info.context.session, data)

        access_token = auth_service.create_access_token(user)
        refresh_token = auth_service.create_refresh_token(user)

        if info.context.response:
            auth_service.set_refresh_token_to_cookie(info.context.response, refresh_token)

        return AuthOutput(
            user=user_service.to_schema(user),
            access_token=access_token,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def logout(self, info: ContextInfo) -> None:
        refresh_token = info.context.request.cookies.get(AuthTokenEnum.REFRESH_TOKEN.value) or ""
        if info.context.response:
            info.context.response.delete_cookie(AuthTokenEnum.REFRESH_TOKEN.value)
        return await auth_service.logout(info.context.session, refresh_token)
