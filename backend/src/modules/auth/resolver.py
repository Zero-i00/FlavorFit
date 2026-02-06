import strawberry

from config.graphql import ContextInfo

from modules.user.schema import UserOutput

from modules.auth.service import auth_service
from modules.auth.schema import AuthInput, AuthOutput

@strawberry.type
class AuthQuery:

    @strawberry.field
    async def me(self, info: ContextInfo) -> UserOutput:
        return await auth_service.me(info.context.session)
    

@strawberry.type
class AuthMutation:

    @strawberry.mutation
    async def login(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        return await auth_service.login(info.context.session, data)
    
    @strawberry.mutation
    async def register(self, info: ContextInfo, data: AuthInput) -> AuthOutput:
        return await auth_service.register(info.context.session, data)
