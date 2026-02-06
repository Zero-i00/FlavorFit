from enum import Enum
from typing import TYPE_CHECKING, List
from database.orm import Base
from database.orm import max_char_field, max_text_field
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, Computed, ForeignKey

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.recipe import RecipeIngredientModel
    from database.models.reaction import CommentModel, FavoriteModel

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
    author: Mapped["UserModel"] = relationship(back_populates="recipes")

    steps: Mapped[List["RecipeCookStepModel"]] = relationship(back_populates="recipe")
    ingredients: Mapped[List["RecipeIngredientModel"]] = relationship(back_populates="recipe")
    comments: Mapped[List["CommentModel"]] = relationship(back_populates="recipe")
    favorites: Mapped[List["FavoriteModel"]] = relationship(back_populates="recipe")


class RecipeCookStepModel(Base):
    __tablename__ = 'recipe_cook_steps'

    order: Mapped[int]
    title: Mapped[max_char_field]
    description: Mapped[max_text_field]

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    recipe: Mapped["RecipeModel"] = relationship(back_populates="steps")
