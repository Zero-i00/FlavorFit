from enum import Enum
from typing import List
from typing import TYPE_CHECKING, Optional

import strawberry
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.orm import Base, max_char_field

if TYPE_CHECKING:
    from database.models.recipe import RecipeModel
    from database.models.order import CartModel, OrderModel
    from database.models.recipe import CommentModel, FavoriteModel


@strawberry.enum
class RoleEnum(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


@strawberry.enum
class GenderEnum(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


@strawberry.enum
class ActivityLevelEnum(Enum):
    SEDENTARY = 'SEDENTARY'
    LIGHT = 'LIGHT'
    MODERATE = 'MODERATE'
    ACTIVE = 'ACTIVE'
    VERY_ACTIVE = 'VERY_ACTIVE'


@strawberry.enum
class NutritionGoalEnum(Enum):
    WEIGHT_LOSS = 'WEIGHT_LOSS'
    MAINTENANCE = 'MAINTENANCE'
    MUSCLE_GAIN = 'MUSCLE_GAIN'


class UserModel(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.USER)

    is_active: Mapped[bool] = mapped_column(default=True)

    profile: Mapped[Optional['ProfileModel']] = relationship(back_populates="user", lazy="selectin")
    cart: Mapped[Optional['CartModel']] = relationship(back_populates='user', lazy="selectin")
    parameters: Mapped[Optional['BodyParameterModel']] = relationship(back_populates="user", lazy="selectin")
    recipes: Mapped[List["RecipeModel"]] = relationship(back_populates="author", lazy="raise_on_sql")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="author", lazy="raise_on_sql")
    orders: Mapped[List["OrderModel"]] = relationship(back_populates="user", lazy="raise_on_sql")
    favorites: Mapped[List["FavoriteModel"]] = relationship(back_populates="author", lazy="raise_on_sql")



class ProfileModel(Base):
    __tablename__ = 'profiles'

    full_name: Mapped[max_char_field]

    age: Mapped[Optional[int]]
    bio: Mapped[Optional[max_char_field]]
    gender: Mapped[Optional[GenderEnum]]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    user: Mapped["UserModel"] = relationship(back_populates="profile", lazy="raise_on_sql")


class BodyParameterModel(Base):
    __tablename__ = 'body_parameters'

    height_cm: Mapped[Optional[float]]
    weight_kg: Mapped[Optional[float]]
    goal_weight_kg: Mapped[Optional[float]]

    arm_cm: Mapped[Optional[float]]
    chest_cm: Mapped[Optional[float]]
    waist_cm: Mapped[Optional[float]]
    thigh_cm: Mapped[Optional[float]]

    activity_level: Mapped[ActivityLevelEnum] = mapped_column(default=ActivityLevelEnum.MODERATE)
    nutrition_goal: Mapped[NutritionGoalEnum] = mapped_column(default=NutritionGoalEnum.MAINTENANCE)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    user: Mapped["UserModel"] = relationship(back_populates="parameters", lazy="raise_on_sql")
