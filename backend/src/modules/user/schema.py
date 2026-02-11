import strawberry
from strawberry import UNSET
from typing import Optional
from database.models.user import RoleEnum
from database.models.user.user import GenderEnum, ActivityLevelEnum, NutritionGoalEnum


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



@strawberry.input
class BodyParameterInput:
    height_cm: Optional[float] = UNSET
    weight_kg: Optional[float] = UNSET
    goal_weight_kg: Optional[float] = UNSET

    arm_cm: Optional[float] = UNSET
    chest_cm: Optional[float] = UNSET
    waist_cm: Optional[float] = UNSET
    thigh_cm: Optional[float] = UNSET

    activity_level: Optional[ActivityLevelEnum] = UNSET
    nutrition_goal: Optional[NutritionGoalEnum] = UNSET


@strawberry.input
class BodyParameterUpdate:
    height_cm: Optional[float] = UNSET
    weight_kg: Optional[float] = UNSET
    goal_weight_kg: Optional[float] = UNSET
    arm_cm: Optional[float] = UNSET
    chest_cm: Optional[float] = UNSET
    waist_cm: Optional[float] = UNSET
    thigh_cm: Optional[float] = UNSET
    activity_level: Optional[ActivityLevelEnum] = UNSET
    nutrition_goal: Optional[NutritionGoalEnum] = UNSET

@strawberry.type
class BodyParameterOutput(BodyParameterInput):
    id: int


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
