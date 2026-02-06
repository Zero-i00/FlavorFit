from enum import Enum
from typing import List
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, Optional
from database.orm import Base, max_char_field
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from database.models.recipe import RecipeModel
    from database.models.order import CartModel, OrderModel
    from database.models.reaction import CommentModel, FavoriteModel


class RoleEnum(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class GenderEnum(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class ActivityLevelEnum(Enum):
    SEDENTARY = 'SEDENTARY'
    LIGHT = 'LIGHT'
    MODERATE = 'MODERATE'
    ACTIVE = 'ACTIVE'
    VERY_ACTIVE = 'VERY_ACTIVE'


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

    profile: Mapped[Optional['ProfileModel']] = relationship(back_populates="user")
    cart: Mapped[Optional['CartModel']] = relationship(back_populates='user')
    parameters: Mapped[Optional['BodyParameterModel']] = relationship(back_populates="user")
    recipes: Mapped[List["RecipeModel"]] = relationship(back_populates="author")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="author")
    orders: Mapped[List["OrderModel"]] = relationship(back_populates="user")
    favorites: Mapped[List["FavoriteModel"]] = relationship(back_populates="author")



class ProfileModel(Base):
    __tablename__ = 'profiles'

    full_name: Mapped[max_char_field]

    age: Mapped[Optional[int]]
    bio: Mapped[Optional[max_char_field]]
    gender: Mapped[Optional[GenderEnum]]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    user: Mapped["UserModel"] = relationship(back_populates="profile")


class BodyParameterModel(Base):
    __tablename__ = 'body_parameters'

    height_cm: Mapped[Optional[float]]
    weight_kg: Mapped[Optional[float]]
    goal_weight_kg: Mapped[Optional[float]]

    arm_cm: Mapped[Optional[float]]
    chest_cm: Mapped[Optional[float]]
    waist_cm: Mapped[Optional[float]]
    thigh_cm: Mapped[Optional[float]]

    activity_level: Mapped[ActivityLevelEnum]
    nutrition_goal: Mapped[NutritionGoalEnum]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    user: Mapped["UserModel"] = relationship(back_populates="parameters")
