import strawberry
from strawberry import UNSET
from typing import Optional
from database.models.user.user import ActivityLevelEnum, NutritionGoalEnum

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


class BodyParameterUpdate(BodyParameterInput):
    pass


@strawberry.type
class BodyParameterOutput(BodyParameterInput):
    id: int
    user_id: int
    activity_level: ActivityLevelEnum = ActivityLevelEnum.MODERATE
    nutrition_goal: NutritionGoalEnum = NutritionGoalEnum.MAINTENANCE
