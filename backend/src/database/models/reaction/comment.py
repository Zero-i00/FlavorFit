from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.orm import Base, max_text_field

if TYPE_CHECKING:
    from database.models.user import UserModel
    from database.models.recipe import RecipeModel


class CommentModel(Base):
    __tablename__ = 'comments'

    content: Mapped[max_text_field]

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    author: Mapped["UserModel"] = relationship(back_populates="comments")

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), index=True)
    recipe: Mapped["RecipeModel"] = relationship(back_populates="comments")
