import strawberry
from typing import Optional
from strawberry import UNSET

from modules.user.schema import UserOutput
from modules.recipe.schema import RecipeOutput

@strawberry.input
class CommentInput:
    content: str
    recipe_id: int
    author_id: int


@strawberry.input
class CommentUpdate:
    content: Optional[str] = UNSET


@strawberry.type
class CommentOutput(CommentInput):
    id: int
    author: UserOutput
    recipe: RecipeOutput
