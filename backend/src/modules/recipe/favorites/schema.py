import strawberry

from modules.user.schema import UserOutput


@strawberry.input
class FavoriteInput:
    recipe_id: int


@strawberry.type
class FavoriteOutput:
    id: int
    author_id: int
    author: UserOutput
    recipe_id: int
