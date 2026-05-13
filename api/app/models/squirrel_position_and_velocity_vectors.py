from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class SquirrelPositionAndVelocityProblem(Base):
    __table_args__ = {"schema": "squirrel_position_and_velocity_vectors"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    a_x: Mapped[float] = mapped_column(Float, nullable=False)
    b_x: Mapped[float] = mapped_column(Float, nullable=False)
    c_y: Mapped[float] = mapped_column(Float, nullable=False)
    time: Mapped[float] = mapped_column(Float, nullable=False)


class SquirrelPositionAndVelocityPartAAttempt(Base):
    __table_args__ = {"schema": "squirrel_position_and_velocity_vectors"}
    __tablename__ = "attempt_a"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("squirrel_position_and_velocity_vectors.problems.id"), nullable=False)
    student_a_x: Mapped[float] = mapped_column(Float, nullable=False)
    student_b_x: Mapped[float] = mapped_column(Float, nullable=False)
    student_c_y: Mapped[float] = mapped_column(Float, nullable=False)
    correct_a_x: Mapped[float] = mapped_column(Float, nullable=False)
    correct_b_x: Mapped[float] = mapped_column(Float, nullable=False)
    correct_c_y: Mapped[float] = mapped_column(Float, nullable=False)
    coefficient_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)


class SquirrelPositionAndVelocityPartBAttempt(Base):
    __table_args__ = {"schema": "squirrel_position_and_velocity_vectors"}
    __tablename__ = "attempt_b"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("squirrel_position_and_velocity_vectors.problems.id"), nullable=False)
    student_distance: Mapped[float] = mapped_column(Float, nullable=False)
    correct_distance: Mapped[float] = mapped_column(Float, nullable=False)
    distance_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)


class SquirrelPositionAndVelocityPartCAttempt(Base):
    __table_args__ = {"schema": "squirrel_position_and_velocity_vectors"}
    __tablename__ = "attempt_c"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("squirrel_position_and_velocity_vectors.problems.id"), nullable=False)
    student_magnitude: Mapped[float] = mapped_column(Float, nullable=False)
    correct_magnitude: Mapped[float] = mapped_column(Float, nullable=False)
    student_direction: Mapped[float] = mapped_column(Float, nullable=False)
    correct_direction: Mapped[float] = mapped_column(Float, nullable=False)
    magnitude_and_direction_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)