from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class DropTimeProblem(Base):
    __table_args__ = {"schema": "drop_time"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    walker_start: Mapped[float] = mapped_column(Float, nullable=False)
    walker_velocity: Mapped[float] = mapped_column(Float, nullable=False)


class DropTimeAttempt(Base):
    __table_args__ = {"schema": "drop_time"}
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("drop_time.problems.id"), nullable=False)
    student_drop_time: Mapped[float] = mapped_column(Float, nullable=False)
    correct_drop_time: Mapped[float] = mapped_column(Float, nullable=False)
    target_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)