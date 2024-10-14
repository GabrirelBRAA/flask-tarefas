from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary, String, Enum
import enum
from pydantic import BaseModel, ConfigDict, field_serializer, Field
from typing import Optional

class TaskStatus(enum.Enum):
    pending = 1
    done = 2

class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="tasks")
    status: Mapped[enum.Enum] = mapped_column(Enum(TaskStatus))

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, description={self.description!r}, status={self.status})"


class TaskScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
    id: Optional[int] = None
    description: str = Field(..., max_length=300, min_length=1)
    status: Optional[TaskStatus] = "pending"

    @field_serializer("status")
    def serialize_group(self, status: TaskStatus, _info):
        return status.name