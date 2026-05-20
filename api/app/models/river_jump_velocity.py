from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class RiverJumpVelocityProblem(Base):
    __table_args__ = {"schema": "river_jump_velocity"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    x_f: Mapped[float] = mapped_column(Float, nullable=False)
    y_i: Mapped[float] = mapped_column(Float, nullable=False)
    y_f: Mapped[float] = mapped_column(Float, nullable=False)


class RiverJumpVelocityPartAAttempt(Base):
    __table_args__ = {"schema": "river_jump_velocity"}
    __tablename__ = "attempt_a"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("river_jump_velocity.problems.id"), nullable=False)
    student_x_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    correct_x_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    velocity_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)


class RiverJumpVelocityPartBAttempt(Base):
    __table_args__ = {"schema": "river_jump_velocity"}
    __tablename__ = "attempt_b"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("river_jump_velocity.problems.id"), nullable=False)
    student_final_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    correct_final_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    final_velocity_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)