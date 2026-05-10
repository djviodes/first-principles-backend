from sqlalchemy import Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class RelayCatchupTimeProblem(Base):
    __table_args__ = {"schema": "relay_catchup_time"}
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    a: Mapped[float] = mapped_column(Float, nullable=False)
    b_one: Mapped[float] = mapped_column(Float, nullable=False)
    b_two: Mapped[float] = mapped_column(Float, nullable=False)
    v_one: Mapped[float] = mapped_column(Float, nullable=False)
    v_two: Mapped[float] = mapped_column(Float, nullable=False)
    s_one: Mapped[float] = mapped_column(Float, nullable=False)
    s_two: Mapped[float] = mapped_column(Float, nullable=False)


class RelayCatchupTimeAttempt(Base):
    __table_args__ = {"schema": "relay_catchup_time"}
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    problem_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("relay_catchup_time.problems.id"), nullable=False)
    student_relay_catchup_time: Mapped[float] = mapped_column(Float, nullable=False)
    correct_relay_catchup_time: Mapped[float] = mapped_column(Float, nullable=False)
    time_hit: Mapped[bool] = mapped_column(Boolean, nullable=False)