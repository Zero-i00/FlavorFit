import strawberry
from typing import Optional
from strawberry import UNSET

from modules.user.schema import UserOutput


@strawberry.input
class CommentInput:
    content: str
    recipe_id: int
    author_id: int


@strawberry.input
class CommentUpdate:
    content: Optional[str] = UNSET


@strawberry.type
class CommentOutput:
    id: int
    content: str
    recipe_id: int
    author_id: int
    author: UserOutput
