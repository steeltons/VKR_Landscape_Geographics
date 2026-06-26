"""SQLAlchemy ORM models for ml-service persistence layer."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    SmallInteger,
    Double,
    String,
    UUID,
    DateTime,
    JSON,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RecommendationFeedbackEntity(Base):
    __tablename__ = "recommendation_feedback"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        default=uuid.uuid4,
    )

    # --- Input data ---
    point_x: Mapped[float] = mapped_column(Double, nullable=False)
    point_y: Mapped[float] = mapped_column(Double, nullable=False)
    task_type: Mapped[str] = mapped_column(String(64), nullable=False)
    target: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # --- Related domain objects ---
    territory_id: Mapped[int] = mapped_column(Integer, nullable=False)
    landscape_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # --- Model result ---
    model_version: Mapped[str] = mapped_column(String(128), nullable=False)
    model_score: Mapped[float] = mapped_column(Double, nullable=False)

    # --- Feature snapshot ---
    features: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # --- Feedback ---
    rating: Mapped[int | None] = mapped_column(
        SmallInteger,
        nullable=True,
    )

    # --- Timestamps ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    rated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 10",
            name="ck_recommendation_feedback_rating_range",
        ),
        Index("idx_feedback_territory_id", "territory_id"),
        Index("idx_feedback_territory_task", "territory_id", "task_type"),
        Index("idx_feedback_rated", "rated_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<RecommendationFeedbackEntity id={self.id} "
            f"request_id={self.request_id} "
            f"territory_id={self.territory_id} "
            f"task_type={self.task_type} "
            f"rating={self.rating}>"
        )
