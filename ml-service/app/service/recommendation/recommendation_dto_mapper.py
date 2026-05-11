from app.service.recommendation.recommendation_dto import (
    EvidenceRsDto,
    ExplanationRsDto,
    RecommendationRsDto,
)


class RecommendationDtoMapper:
    @staticmethod
    def to_rs_dto(data: dict) -> RecommendationRsDto:
        explanation = data.get("explanation", {})

        return RecommendationRsDto(
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