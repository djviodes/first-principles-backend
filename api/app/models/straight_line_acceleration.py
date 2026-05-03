from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class StraightLineAccelerationProblem(Base):
    __table_args__ = {"schema": "straight_line_acceleration"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    distance: Mapped[float] = mapped_column(Float, nullable=False)
    time: Mapped[float] = mapped_column(Float, nullable=False)


class StraightLineAccelerationAttempt(Base):
    __table_args__ = {"schema": "straight_line_acceleration"}
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("straight_line_acceleration.problems.id"), nullable=False)
    student_straight_line_acceleration: Mapped[float] = mapped_column(Float, nullable=False)
    correct_straight_line_acceleration: Mapped[float] = mapped_column(Float, nullable=False)
    time_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)