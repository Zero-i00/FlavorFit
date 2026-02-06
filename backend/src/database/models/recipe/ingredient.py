from enum import Enum
from typing import TYPE_CHECKING, List
from database.orm import Base
from database.orm import max_char_field, max_text_field
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint

if TYPE_CHECKING:
    from database.models.recipe import RecipeModel
    from database.models.order import CartItem


class IngredientUnitEnum(Enum):
    GRAM = 'GRAM'
    PIECE = 'PIECE'
    CLOVES = 'CLOVES'
    TEASPOON = 'TEASPOON'
    TABLESPOON = 'TABLESPOON'
    MILLILITER = 'MILLILITER'


class IngredientModel(Base):
    __tablename__ = 'ingredients'
    __table_args__ = (
        CheckConstraint('price >= 0', name='ck_ingredient_price_positive'),
    )

    icon: Mapped[str]
    price: Mapped[float]
    name: Mapped[max_char_field]
    description: Mapped[max_text_field]
    initial_unit: Mapped[IngredientUnitEnum]

    recipes: Mapped[List["RecipeIngredientModel"]] = relationship(back_populates="ingredient")
    cart_items: Mapped[List["CartItem"]] = relationship(back_populates="ingredient")


class RecipeIngredientModel(Base):
    __tablename__ = 'recipe_ingredients'
    __table_args__ = (
        UniqueConstraint('recipe_id', 'ingredient_id', name='uq_recipe_ingredient'),
        CheckConstraint('quantity > 0', name='ck_recipe_ingredient_quantity_positive'),
    )

    quantity: Mapped[float]
    unit: Mapped[IngredientUnitEnum]

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    recipe: Mapped["RecipeModel"] = relationship(back_populates="ingredients")

    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), index=True)
    ingredient: Mapped["IngredientModel"] = relationship(back_populates="recipes")
