from database.orm import Base
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.recipe import IngredientModel
    from database.models.order import OrderModel


class CartModel(Base):
    __tablename__ = 'carts'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    user: Mapped["UserModel"] = relationship(back_populates="cart")

    items: Mapped[List["CartItem"]] = relationship(back_populates="cart", lazy="selectin")
    order: Mapped[Optional["OrderModel"]] = relationship(back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'
    __table_args__ = (
        UniqueConstraint('cart_id', 'ingredient_id', name='uq_cart_item'),
        CheckConstraint('quantity > 0', name='ck_cart_item_quantity_positive'),
    )

    quantity: Mapped[int] = mapped_column(default=1)

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), index=True)
    cart: Mapped["CartModel"] = relationship(back_populates="items")

    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), index=True)
    ingredient: Mapped["IngredientModel"] = relationship(back_populates="cart_items")
