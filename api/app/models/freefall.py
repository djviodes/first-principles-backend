from sqlalchemy import Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db import Base


class FreeFall(Base):
    __tablename__ = "freefall"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    drag: Mapped[bool] = mapped_column(Boolean, nullable=False)
    initial_height: Mapped[float] = mapped_column(Float, nullable=False)
    initial_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    final_velocity: Mapped[float] = mapped_column(Float, nullable=False)
    acceleration: Mapped[float] = mapped_column(Float, nullable=False)
    time_of_flight: Mapped[float] = mapped_column(Float, nullable=False)