from typing import List, Optional

import strawberry
from fastapi import (
    status,
    HTTPException
)

from database.models import RoleEnum
from config.graphql import ContextInfo
from modules.auth.guards import HasRole, IsAuthenticated
from modules.reaction.comments.schema import CommentOutput, CommentInput, CommentUpdate
from modules.reaction.comments.service import comment_service


@strawberry.type
class CommentQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def list(self, info: ContextInfo) -> List[CommentOutput]:
        return await comment_service.list(info.context.session)

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def retrieve(self, info: ContextInfo, id: int) -> Optional[CommentOutput]:
        return await comment_service.retrieve(info.context.session, id)


@strawberry.type
class CommentMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create(self, info: ContextInfo, obj: CommentInput) -> CommentOutput:
        return await comment_service.create(info.context.session, obj)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, id: int, obj: CommentUpdate) -> CommentOutput:
        updated = await comment_service.update(info.context.session, id, obj)
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Не удалось найти комментарий"
            )

        return updated

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def destroy(self, info: ContextInfo, id: int) -> None:
        return await comment_service.destroy(info.context.session, id)