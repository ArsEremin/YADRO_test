from enum import StrEnum

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[Gender]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    location: Mapped[str]
    photo: Mapped[str]
    profile_url: Mapped[str] = mapped_column(unique=True)
