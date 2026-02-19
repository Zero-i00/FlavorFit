from database.orm import Base
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.recipe import RecipeModel


class FavoriteModel(Base):
    __tablename__ = 'favorites'
    __table_args__ = (
        UniqueConstraint('author_id', 'recipe_id', name='uq_favorite_user_recipe'),
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped["UserModel"] = relationship(back_populates="favorites", lazy='selectin')

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    recipe: Mapped["RecipeModel"] = relationship(back_populates="favorites", lazy='selectin')
