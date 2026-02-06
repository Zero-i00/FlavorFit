import datetime
from typing import Annotated
from sqlalchemy import String, text
from config.constants import MAX_CHAR_FIELD, MAX_TEXT_FIELD
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

max_char_field = Annotated[str, MAX_CHAR_FIELD]
max_text_field = Annotated[str, MAX_TEXT_FIELD]

class Base(DeclarativeBase):

    type_annotation_map = {
        max_char_field: String(MAX_CHAR_FIELD),
        max_text_field: String(MAX_TEXT_FIELD),
    }

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
