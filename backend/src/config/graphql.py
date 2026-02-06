from fastapi import Depends
from strawberry import Info
from database.session import get_session
from strawberry.fastapi import BaseContext
from sqlalchemy.ext.asyncio import AsyncSession

class GraphQLContext(BaseContext):
    def __init__(self, session: AsyncSession):
        self.session = session


async def get_graphql_context(session=Depends(get_session)) -> GraphQLContext:
    return GraphQLContext(session=session)


ContextInfo = Info[GraphQLContext, None]
