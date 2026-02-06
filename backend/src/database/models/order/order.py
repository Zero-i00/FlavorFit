import strawberry
from enum import Enum
from typing import TYPE_CHECKING, Optional
from database.orm import Base, max_text_field
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.order import CartModel


@strawberry.enum
class OrderStatusEnum(Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class OrderModel(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='ck_order_total_amount_positive'),
    )

    order_id: Mapped[str] = mapped_column(unique=True)
    status: Mapped[OrderStatusEnum] = mapped_column(default=OrderStatusEnum.PENDING)
    total_amount: Mapped[float]

    comment: Mapped[Optional[max_text_field]]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["UserModel"] = relationship(back_populates="orders")

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), unique=True)
    cart: Mapped["CartModel"] = relationship(back_populates="order")
