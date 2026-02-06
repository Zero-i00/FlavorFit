from database.orm import Base, max_char_field
from sqlalchemy.orm import Mapped, mapped_column


class CourierModel(Base):
    __tablename__ = 'couriers'

    full_name: Mapped[max_char_field]
    phone: Mapped[max_char_field] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)


