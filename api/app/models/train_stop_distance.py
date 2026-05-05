from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class TrainStopDistanceProblem(Base):
    __table_args__ = {"schema": "train_stop_distance"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    velocity: Mapped[float] = mapped_column(Float, nullable=False)
    acceleration: Mapped[float] = mapped_column(Float, nullable=False)


class TrainStopDistanceAttempt(Base):
    __table_args__ = {"schema": "train_stop_distance"}
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("train_stop_distance.problems.id"), nullable=False)
    student_train_stop_distance: Mapped[float] = mapped_column(Float, nullable=False)
    correct_train_stop_distance: Mapped[float] = mapped_column(Float, nullable=False)
    distance_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)