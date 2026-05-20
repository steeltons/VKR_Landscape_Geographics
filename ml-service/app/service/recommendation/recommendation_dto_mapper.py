from uuid import UUID

from app.service.recommendation.recommendation_dto import (
    EvidenceRsDto,
    ExplanationRsDto,
    FeedbackRsDto,
    RecommendationRsDto,
)
from app.persistence.models import RecommendationFeedbackEntity


class RecommendationDtoMapper:
    @staticmethod
    def to_rs_dto(data: dict) -> RecommendationRsDto:
        explanation = data.get("explanation", {})

        return RecommendationRsDto(
            request_id=data.get("request_id"),
            score=round(float(data.get("score", 0.0)), 4),
            level=data.get("level", ""),
            recommendation=data.get("recommendation", ""),
            explanation=ExplanationRsDto(
                summary=explanation.get("summary", ""),
                reasons=explanation.get("reasons", []),
                warnings=explanation.get("warnings", []),
                evidence=[
                    EvidenceRsDto(**item)
                    for item in explanation.get("evidence", [])
                    if item.get("object_id") is not None
                ],
            ),
        )

    @staticmethod
    def feedback_to_rs_dto(data: dict) -> FeedbackRsDto:
        """Convert feedback result dict to FeedbackRsDto."""
        return FeedbackRsDto(
            request_id=data["request_id"],
            rating=data.get("rating"),
            rated_at=data.get("rated_at", ""),
            message="Спасибо за оценку!" if data.get("rating") is not None else "",
        )
