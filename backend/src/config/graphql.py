from typing import Optional
from strawberry import Info
from fastapi import Depends, Request
from database.session import get_session
from modules.user.schema import UserOutput
from strawberry.fastapi import BaseContext
from modules.auth.service import auth_service
from modules.user.service import user_service
from sqlalchemy.ext.asyncio import AsyncSession

class GraphQLContext(BaseContext):
    def __init__(self, request: Request, session: AsyncSession, user: Optional[UserOutput]):
        self.session = session
        self.request = request
        self.user = user


async def get_graphql_context(
    request: Request,
    session=Depends(get_session)
) -> GraphQLContext:
    try:
        payload = auth_service.get_authorized_user(request)
        print(payload)

        user_id = payload.get('user_id', None)
        if user_id is None:
            raise ValueError("user_id not found in token")

        user = await user_service.retrieve(session, int(user_id))
    except Exception:
        user = None

    return GraphQLContext(request=request, session=session, user=user)


ContextInfo = Info[GraphQLContext, None]
