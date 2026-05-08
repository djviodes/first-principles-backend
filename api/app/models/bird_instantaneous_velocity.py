from sqlalchemy import Boolean, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from datetime import datetime
import uuid

from app.db import Base


class BirdInstantaneousVelocityProblem(Base):
    __table_args__ = {"schema": "bird_instantaneous_velocity"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    function_type: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[float] = mapped_column(Float, nullable=False)
    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)
    c: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    d: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class BirdInstantaneousVelocityAttempt(Base):
    __table_args__ = {"schema": "bird_instantaneous_velocity"}
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bird_instantaneous_velocity.problems.id"), nullable=False)
    student_bird_instantaneous_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    correct_bird_instantaneous_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    velocity_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)