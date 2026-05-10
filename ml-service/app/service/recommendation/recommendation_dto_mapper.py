from app.service.recommendation.recommendation_dto import RecommendationRsDto, ExplanationRsDto


class RecommendationDtoMapper:

    @staticmethod
    def to_rs_dto(data: dict) -> RecommendationRsDto:
        explanation = data.get("explanation", {})

        return RecommendationRsDto(
            score=data.get("score", 0.0),
            explanation=ExplanationRsDto(
                summary=explanation.get("summary", ""),
                reasons=explanation.get("reasons", []),
                warnings=explanation.get("warnings", []),
            ),
        )