from typing import Optional
import strawberry
from database.models.user import RoleEnum

@strawberry.input
class UserInput:
    email: str
    password: str
    is_active: bool = True
    role: RoleEnum = RoleEnum.USER


@strawberry.input
class UserUpdate:
    email: Optional[str]

@strawberry.type
class UserOutput:
    id: int
    role: str
    email: str
    is_active: bool
