from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary, String
from typing import List

from pydantic import BaseModel, Field, field_validator, ConfigDict
import re

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[bytearray] = mapped_column(LargeBinary(length=60))
    password_salt: Mapped[bytearray] = mapped_column(LargeBinary(length=60))
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    @staticmethod
    def exists(name: str) -> bool:
        return User.query.filter(User.name == name).first() is not None


#https://stackoverflow.com/questions/5142103/regex-to-validate-password-strength
password_regex = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

class UserScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    name: str = Field(..., max_length=100)
    password: str = Field(...)

    @field_validator('password')
    def validate_password(cls, v: str) -> str:
        if re.fullmatch(password_regex, v):
            return v
        else:
            raise ValueError('password must contain 8 characters, 1 uppercase, 1 lowercase, a number and a special character!')

