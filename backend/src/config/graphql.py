from typing import Optional
from strawberry import Info
from fastapi import Depends, Request
from database.session import get_session
from database.models.user import UserModel
from strawberry.fastapi import BaseContext
from modules.auth.service import auth_service
from modules.auth.schema import AuthTokenEnum
from modules.user.service import user_service
from sqlalchemy.ext.asyncio import AsyncSession


class GraphQLContext(BaseContext):
    def __init__(self, request: Request, session: AsyncSession, user: Optional[UserModel]):
        self.session = session
        self.request = request
        self.user = user


async def get_graphql_context(
    request: Request,
    session=Depends(get_session)
) -> GraphQLContext:
    try:
        payload = auth_service.get_token_payload(
            request=request, 
            token_type=AuthTokenEnum.ACCESS_TOKEN
        )

        user_id = payload.get('user_id', None)
        if user_id is None:
            raise ValueError("user_id not found in token")

        user = await user_service.retrieve(session, int(user_id))
    except Exception:
        user = None

    return GraphQLContext(request=request, session=session, user=user)


ContextInfo = Info[GraphQLContext, None]
