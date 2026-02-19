import strawberry
from enum import Enum
from database.orm import Base
from typing import TYPE_CHECKING, List
from sqlalchemy.event import listens_for
from database.orm import max_char_field, max_text_field
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Computed, ForeignKey

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.recipe import RecipeIngredientModel
    from database.models.reaction import CommentModel, FavoriteModel

@strawberry.enum
class RecipeTypeEnum(Enum):
    FIRST = 'FIRST'
    SECOND = 'SECOND'
    DRINK = 'DRINK'
    SALAD = 'SALAD'
    BAKERY = 'BAKERY'
    DESSERT = 'DESSERT'
    STARTER = 'STARTER'
    HOT_APPETIZERS = 'HOT_APPETIZERS'
    COLD_APPETIZERS = 'COLD_APPETIZERS'


@strawberry.enum
class RecipeDifficultyEnum(Enum):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'


class RecipeModel(Base):
    __tablename__ = 'recipes'
    __table_args__ = (
        CheckConstraint('cook_time >= 0', name='ck_recipe_cook_time_positive'),
        CheckConstraint('prepare_time >= 0', name='ck_recipe_prepare_time_positive'),
        CheckConstraint('serving_time >= 0', name='ck_recipe_serving_time_positive'),
        CheckConstraint('fats >= 0', name='ck_recipe_fats_positive'),
        CheckConstraint('carbs >= 0', name='ck_recipe_carbs_positive'),
        CheckConstraint('proteins >= 0', name='ck_recipe_proteins_positive'),
    )

    title: Mapped[max_char_field]
    description: Mapped[max_text_field]
    slug: Mapped[str] = mapped_column(unique=True, index=True)

    cook_time: Mapped[int]
    prepare_time: Mapped[int]
    serving_time: Mapped[int]

    fats: Mapped[float]
    carbs: Mapped[float]
    proteins: Mapped[float]

    type: Mapped[RecipeTypeEnum]
    difficulty: Mapped[RecipeDifficultyEnum]

    calories: Mapped[float] = mapped_column(
        Computed(
            "fats * 9 + proteins * 4 + carbs * 4",
            persisted=True
        )
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped["UserModel"] = relationship(back_populates="recipes", lazy="selectin")

    steps: Mapped[List["RecipeCookStepModel"]] = relationship(back_populates="recipe", lazy="selectin")
    ingredients: Mapped[List["RecipeIngredientModel"]] = relationship(back_populates="recipe", lazy="selectin")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="recipe")
    favorites: Mapped[List["FavoriteModel"]] = relationship(back_populates="recipe")



class RecipeCookStepModel(Base):
    __tablename__ = 'recipe_cook_steps'

    order: Mapped[int]
    title: Mapped[max_char_field]
    description: Mapped[max_text_field]

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    recipe: Mapped["RecipeModel"] = relationship(back_populates="steps")
