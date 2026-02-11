import strawberry
from strawberry import UNSET
from typing import Optional
from database.models.user import RoleEnum
from modules.user.profile.schema import ProfileUpdate, ProfileOutput
from modules.user.parameters.schema import BodyParameterUpdate, BodyParameterOutput


@strawberry.input
class UserInput:
    email: str
    password: str
    is_active: bool = True
    role: RoleEnum = RoleEnum.USER


@strawberry.input
class UserUpdate:
    email: Optional[str] = UNSET
    password: Optional[str] = UNSET

    profile: Optional[ProfileUpdate] = UNSET
    parameters: Optional[BodyParameterUpdate] = UNSET


@strawberry.type
class UserOutput:
    id: int
    role: str
    email: str
    is_active: bool

    profile: Optional[ProfileOutput] = UNSET
    parameters: Optional[BodyParameterOutput] = UNSET
