from typing import List, Optional

import strawberry
from fastapi import status, HTTPException

from database.models import RoleEnum
from config.graphql import ContextInfo
from modules.auth.guards import HasRole, IsAuthenticated
from modules.recipe.comments.schema import CommentOutput, CommentInput, CommentUpdate
from modules.recipe.comments.service import comment_service


@strawberry.type
class CommentQuery:

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def list(self, info: ContextInfo) -> List[CommentOutput]:
        comments = await comment_service.list(info.context.session)
        return [comment_service.to_schema(c) for c in comments]

    @strawberry.field(permission_classes=[HasRole(RoleEnum(RoleEnum.ADMIN))])
    async def retrieve(self, info: ContextInfo, comment_id: int) -> CommentOutput:
        comment = await comment_service.retrieve(info.context.session, comment_id)
        return comment_service.to_schema(comment)


@strawberry.type
class CommentMutation:

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create(self, info: ContextInfo, obj: CommentInput) -> CommentOutput:
        comment = await comment_service.create(info.context.session, obj)
        return comment_service.to_schema(comment)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update(self, info: ContextInfo, comment_id: int, obj: CommentUpdate) -> CommentOutput:
        comment = await comment_service.update(info.context.session, comment_id, obj)
        return comment_service.to_schema(comment)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def destroy(self, info: ContextInfo, comment_id: int) -> bool:
        return await comment_service.destroy(info.context.session, comment_id)
