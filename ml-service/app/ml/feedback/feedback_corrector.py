"""Feedback-aware score corrector.

Adjusts model predictions based on accumulated user feedback.
Provides a soft, confidence-weighted correction that converges
towards the average user rating as more feedback is collected.
"""

import logging
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.configs.config import settings


logger = logging.getLogger(__name__)


class FeedbackCorrector:
    """Adjusts raw model scores using aggregated user feedback.

    The correction is conservative:
      - maximum contribution of user feedback to the final score is capped
      - confidence grows asymptotically with the number of ratings
    """

    # --- Tunable hyper-parameters ---
    MAX_FEEDBACK_INFLUENCE: float = 0.3
    """Maximum fraction the final score may be pulled toward user average."""

    CONFIDENCE_HALF_LIFE: int = 5
    """Number of ratings at which confidence = 0.5 (sigmoid midpoint)."""

    def __init__(self) -> None:
        self.engine = create_engine(settings.database_url)
        self.session_factory = sessionmaker(bind=self.engine)

    def correct(
        self,
        *,
        territory_id: int,
        task_type: str,
        base_score: float,
    ) -> float:
        """Return a feedback-adjusted score in [0, 1].

        Parameters
        ----------
        territory_id : int
            The territory identifier from the dictionary service.
        task_type : str
            One of ``agriculture``, ``construction``, ``ecology``.
        base_score : float
            Raw model prediction in [0, 1].

        Returns
        -------
        float
            Corrected score in [0, 1].
        """
        feedback_stats = self._load_feedback_stats(
            territory_id=territory_id,
            task_type=task_type,
        )

        if feedback_stats is None or feedback_stats["count"] == 0:
            return base_score

        count: int = feedback_stats["count"]
        avg_rating: float = feedback_stats["avg_rating"]
        user_score: float = avg_rating / 10.0

        confidence = count / (count + self.CONFIDENCE_HALF_LIFE)
        influence = confidence * self.MAX_FEEDBACK_INFLUENCE

        corrected = base_score * (1.0 - influence) + user_score * influence

        corrected = max(0.0, min(corrected, 1.0))

        if abs(corrected - base_score) > 0.005:
            logger.info(
                "FeedbackCorrector: territory=%s task=%s base=%.4f corrected=%.4f "
                "influence=%.4f confidence=%.4f ratings=%s avg=%.4f",
                territory_id,
                task_type,
                base_score,
                corrected,
                influence,
                confidence,
                count,
                avg_rating,
            )

        return corrected

    def _load_feedback_stats(
        self,
        *,
        territory_id: int,
        task_type: str,
    ) -> dict[str, Any] | None:
        """Load aggregated feedback for a territory + task_type pair."""
        query = text("""
            SELECT
                COUNT(*)::int                        AS count,
                AVG(rating)::double precision         AS avg_rating
            FROM recommendation_feedback
            WHERE territory_id   = :territory_id
              AND task_type      = :task_type
              AND rating IS NOT NULL
        """)

        try:
            with self.session_factory() as session:
                row = session.execute(
                    query,
                    {
                        "territory_id": territory_id,
                        "task_type": task_type,
                    },
                ).fetchone()

                if row is None or row.count == 0:
                    return None

                return {
                    "count": row.count,
                    "avg_rating": row.avg_rating,
                }

        except Exception:
            logger.exception(
                "FeedbackCorrector: failed to load feedback stats "
                "territory=%s task=%s",
                territory_id,
                task_type,
            )
            return None
