import strawberry
from database.models.user import RoleEnum

@strawberry.input
class UserInput:
    email: str
    password: str
    role: RoleEnum = RoleEnum.USER
    is_active: bool = True


@strawberry.type
class UserOutput:
    id: int
    email: str
    role: RoleEnum
    is_active: bool
