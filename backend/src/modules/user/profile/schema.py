import strawberry
from strawberry import UNSET
from typing import Optional
from database.models.user.user import GenderEnum

@strawberry.input
class ProfileInput:
    full_name: str
    age: Optional[int] = UNSET
    bio: Optional[str] = UNSET
    user_id: Optional[int] = UNSET
    gender: Optional[GenderEnum] = UNSET


@strawberry.input
class ProfileUpdate:
    full_name: Optional[str] = UNSET
    age: Optional[int] = UNSET
    bio: Optional[str] = UNSET
    gender: Optional[GenderEnum] = UNSET


@strawberry.type
class ProfileOutput(ProfileInput):
    id: int