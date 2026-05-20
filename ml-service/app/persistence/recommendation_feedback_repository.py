"""Repository for recommendation_feedback table operations."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session, sessionmaker

from app.configs.config import settings
from app.persistence.models import RecommendationFeedbackEntity


logger = logging.getLogger(__name__)


class RecommendationFeedbackRepository:
    """Data access layer for recommendation feedback.

    Uses a dedicated engine connected to the training database.
    Each method creates its own session for simplicity and thread safety.
    """

    def __init__(self) -> None:
        self.engine = create_engine(settings.database_url)
        self.session_factory = sessionmaker(bind=self.engine)

    def create(
        self,
        *,
        request_id: uuid.UUID,
        point_x: float,
        point_y: float,
        task_type: str,
        target: str | None,
        territory_id: int,
        landscape_id: int | None,
        model_version: str,
        model_score: float,
        features: dict[str, float] | None = None,
    ) -> RecommendationFeedbackEntity:
        """Create a new feedback record with initial data (rating = NULL)."""
        logger.info(
            "START RecommendationFeedbackRepository::create request_id=%s",
            request_id,
        )

        now = datetime.now(timezone.utc)

        entity = RecommendationFeedbackEntity(
            request_id=request_id,
            point_x=point_x,
            point_y=point_y,
            task_type=task_type,
            target=target,
            territory_id=territory_id,
            landscape_id=landscape_id,
            model_version=model_version,
            model_score=model_score,
            features=features,
            rating=None,
            created_at=now,
            updated_at=now,
        )

        with self.session_factory() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)

        logger.info(
            "END RecommendationFeedbackRepository::create request_id=%s id=%s",
            request_id,
            entity.id,
        )

        return entity

    def get_by_request_id(
        self,
        *,
        request_id: uuid.UUID,
    ) -> RecommendationFeedbackEntity | None:
        """Find a feedback record by request_id."""
        logger.debug(
            "START RecommendationFeedbackRepository::get_by_request_id request_id=%s",
            request_id,
        )

        with self.session_factory() as session:
            entity = session.query(RecommendationFeedbackEntity).filter(
                RecommendationFeedbackEntity.request_id == request_id,
            ).first()

        logger.debug(
            "END RecommendationFeedbackRepository::get_by_request_id request_id=%s found=%s",
            request_id,
            entity is not None,
        )

        return entity

    def update_rating(
        self,
        *,
        request_id: uuid.UUID,
        rating: int,
    ) -> RecommendationFeedbackEntity | None:
        """Set user rating for a recommendation request."""
        logger.info(
            "START RecommendationFeedbackRepository::update_rating request_id=%s rating=%s",
            request_id,
            rating,
        )

        now = datetime.now(timezone.utc)

        with self.session_factory() as session:
            entity = session.query(RecommendationFeedbackEntity).filter(
                RecommendationFeedbackEntity.request_id == request_id,
            ).first()

            if entity is None:
                logger.warning(
                    "END RecommendationFeedbackRepository::update_rating request_id=%s not_found",
                    request_id,
                )
                return None

            entity.rating = rating
            entity.rated_at = now
            entity.updated_at = now

            session.commit()
            session.refresh(entity)

        logger.info(
            "END RecommendationFeedbackRepository::update_rating request_id=%s success",
            request_id,
        )

        return entity

    def update_model_result(
        self,
        *,
        request_id: uuid.UUID,
        model_version: str,
        model_score: float,
        features: dict[str, float] | None = None,
    ) -> RecommendationFeedbackEntity | None:
        """Update model result fields after pipeline execution.

        This is used when the record was created before the pipeline ran
        (two-phase save).
        """
        logger.debug(
            "START RecommendationFeedbackRepository::update_model_result request_id=%s",
            request_id,
        )

        now = datetime.now(timezone.utc)

        with self.session_factory() as session:
            entity = session.query(RecommendationFeedbackEntity).filter(
                RecommendationFeedbackEntity.request_id == request_id,
            ).first()

            if entity is None:
                logger.warning(
                    "END RecommendationFeedbackRepository::update_model_result request_id=%s not_found",
                    request_id,
                )
                return None

            entity.model_version = model_version
            entity.model_score = model_score
            entity.features = features
            entity.updated_at = now

            session.commit()
            session.refresh(entity)

        logger.debug(
            "END RecommendationFeedbackRepository::update_model_result request_id=%s success",
            request_id,
        )

        return entity
